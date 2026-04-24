"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const http = require("node:http");
const os = require("node:os");
const path = require("node:path");
const test = require("node:test");

const { createMockLegacyServer, findFixture, loadFixtures } = require("../server");

function makeTempFixtureRoot() {
  return fs.mkdtempSync(path.join(os.tmpdir(), "hub-mock-legacy-"));
}

function writeFixture(root, relativePath, fixture) {
  const fixturePath = path.join(root, relativePath);
  fs.mkdirSync(path.dirname(fixturePath), { recursive: true });
  fs.writeFileSync(fixturePath, JSON.stringify(fixture, null, 2));
}

function listen(server) {
  return new Promise((resolve) => {
    server.listen(0, "127.0.0.1", () => {
      const address = server.address();
      assert.equal(typeof address, "object");
      resolve(`http://127.0.0.1:${address.port}`);
    });
  });
}

function close(server) {
  return new Promise((resolve, reject) => {
    server.close((error) => (error ? reject(error) : resolve()));
  });
}

test("fixture exists -> returns captured status, headers, and body", async () => {
  const root = makeTempFixtureRoot();
  writeFixture(root, "core/health.json", {
    request: { method: "GET", path_pattern: "/api/health" },
    response_status: 200,
    response_headers: { "x-captured": "yes", "content-length": "999" },
    response_body: { ok: true, data: { status: "ok" } },
  });

  const server = createMockLegacyServer({ fixtureRoot: root });
  const baseUrl = await listen(server);
  try {
    const response = await fetch(`${baseUrl}/api/health?tenant=sprint_mode`, {
      headers: { cookie: "hub_session=abc" },
    });
    assert.equal(response.status, 200);
    assert.equal(response.headers.get("x-captured"), "yes");
    assert.equal(response.headers.get("content-length"), null);
    assert.deepEqual(await response.json(), { ok: true, data: { status: "ok" } });
  } finally {
    await close(server);
  }
});

test("missing fixture -> exact 501 envelope", async () => {
  const root = makeTempFixtureRoot();
  const server = createMockLegacyServer({ fixtureRoot: root });
  const baseUrl = await listen(server);
  try {
    const response = await fetch(`${baseUrl}/api/missing?tenant=sprint_mode`);
    assert.equal(response.status, 501);
    assert.deepEqual(await response.json(), {
      ok: false,
      error: "mock not captured: GET /api/missing",
    });
  } finally {
    await close(server);
  }
});

test("wildcard fixtures use most-specific route", () => {
  const fixtures = [
    { method: "GET", pathPattern: "/api/*", responseBody: { route: "default" } },
    { method: "GET", pathPattern: "/api/reports/*", responseBody: { route: "reports" } },
  ];

  assert.equal(findFixture(fixtures, "GET", "/api/reports/weekly").responseBody.route, "reports");
  assert.equal(findFixture(fixtures, "GET", "/api/other").responseBody.route, "default");
});

test("SSE fixtures replay captured events", async () => {
  const root = makeTempFixtureRoot();
  writeFixture(root, "stream/events.json", {
    request: { method: "GET", path_pattern: "/api/events" },
    response_status: 200,
    response_events: [
      { event: "status", data: { step: "one" }, delay_ms: 1 },
      { event: "done", data: "[DONE]", delay_ms: 1 },
    ],
  });

  const server = createMockLegacyServer({ fixtureRoot: root, sseDelayMs: 1 });
  const baseUrl = await listen(server);
  try {
    const response = await fetch(`${baseUrl}/api/events`);
    assert.equal(response.status, 200);
    assert.match(response.headers.get("content-type"), /^text\/event-stream/);
    const body = await response.text();
    assert.match(body, /event: status\ndata: {"step":"one"}/);
    assert.match(body, /event: done\ndata: \[DONE\]/);
  } finally {
    await close(server);
  }
});

test("server never makes outbound http requests", async () => {
  const root = makeTempFixtureRoot();
  const originalRequest = http.request;
  const originalGet = http.get;
  let outboundCalls = 0;
  http.request = function blockedRequest() {
    outboundCalls += 1;
    throw new Error("outbound http.request is forbidden");
  };
  http.get = function blockedGet() {
    outboundCalls += 1;
    throw new Error("outbound http.get is forbidden");
  };

  const server = createMockLegacyServer({ fixtureRoot: root });
  const baseUrl = await listen(server);
  try {
    const response = await fetch(`${baseUrl}/api/missing`);
    assert.equal(response.status, 501);
    assert.equal(outboundCalls, 0);
  } finally {
    http.request = originalRequest;
    http.get = originalGet;
    await close(server);
  }
});

test("loadFixtures rejects mid-path wildcards", () => {
  const root = makeTempFixtureRoot();
  writeFixture(root, "bad.json", {
    request: { method: "GET", path_pattern: "/api/*/bad" },
    response_body: {},
  });

  assert.throws(() => loadFixtures(root), /wildcard is only supported as a suffix/);
});
