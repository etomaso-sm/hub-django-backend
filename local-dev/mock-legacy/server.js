#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const http = require("node:http");
const path = require("node:path");

const DEFAULT_FIXTURE_ROOT = path.resolve(process.cwd(), "tests/fixtures");
const DEFAULT_PORT = 8787;
const DEFAULT_SSE_DELAY_MS = 50;
const HOP_BY_HOP_HEADERS = new Set([
  "connection",
  "content-encoding",
  "content-length",
  "keep-alive",
  "proxy-authenticate",
  "proxy-authorization",
  "te",
  "trailer",
  "transfer-encoding",
  "upgrade",
]);

function walkJsonFiles(root) {
  if (!fs.existsSync(root)) {
    return [];
  }

  const out = [];
  const entries = fs.readdirSync(root, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(root, entry.name);
    if (entry.isDirectory()) {
      out.push(...walkJsonFiles(fullPath));
    } else if (entry.isFile() && entry.name.endsWith(".json")) {
      out.push(fullPath);
    }
  }
  return out;
}

function normalizeMethod(value) {
  return String(value || "GET").toUpperCase();
}

function validatePattern(pattern, fixturePath) {
  if (typeof pattern !== "string" || !pattern.startsWith("/")) {
    throw new Error(`${fixturePath} request.path_pattern must be an absolute path`);
  }
  if (pattern.slice(0, -1).includes("*")) {
    throw new Error(`${fixturePath} wildcard is only supported as a suffix`);
  }
}

function loadFixtures(fixtureRoot = DEFAULT_FIXTURE_ROOT) {
  const fixtures = [];
  for (const fixturePath of walkJsonFiles(fixtureRoot)) {
    const raw = JSON.parse(fs.readFileSync(fixturePath, "utf8"));
    const request = raw.request || {};
    const pattern = request.path_pattern || request.path;
    validatePattern(pattern, fixturePath);
    fixtures.push({
      method: normalizeMethod(request.method),
      pathPattern: pattern,
      fixturePath,
      responseStatus: Number(raw.response_status || raw.status || 200),
      responseHeaders: raw.response_headers || {},
      responseBody: raw.response_body,
      responseEvents: raw.response_events,
    });
  }
  return fixtures.sort((a, b) => b.pathPattern.replace(/\*$/, "").length - a.pathPattern.replace(/\*$/, "").length);
}

function pathMatches(pattern, requestPath) {
  if (pattern.endsWith("*")) {
    return requestPath.startsWith(pattern.slice(0, -1));
  }
  return requestPath === pattern;
}

function findFixture(fixtures, method, requestPath) {
  const normalizedMethod = normalizeMethod(method);
  return fixtures
    .filter(
      (fixture) =>
        fixture.method === normalizedMethod && pathMatches(fixture.pathPattern, requestPath),
    )
    .sort(
      (a, b) =>
        b.pathPattern.replace(/\*$/, "").length - a.pathPattern.replace(/\*$/, "").length,
    )[0];
}

function sanitizeHeaders(headers) {
  const out = {};
  for (const [key, value] of Object.entries(headers || {})) {
    const normalizedKey = key.toLowerCase();
    if (!HOP_BY_HOP_HEADERS.has(normalizedKey)) {
      out[key] = value;
    }
  }
  return out;
}

function writeJson(res, status, body, headers = {}) {
  res.writeHead(status, {
    "content-type": "application/json; charset=utf-8",
    ...sanitizeHeaders(headers),
  });
  res.end(JSON.stringify(body));
}

function formatSseEvent(event) {
  const lines = [];
  if (event.id !== undefined) {
    lines.push(`id: ${event.id}`);
  }
  if (event.event !== undefined) {
    lines.push(`event: ${event.event}`);
  }
  if (event.retry !== undefined) {
    lines.push(`retry: ${event.retry}`);
  }

  const data = typeof event.data === "string" ? event.data : JSON.stringify(event.data ?? {});
  for (const line of data.split(/\r?\n/)) {
    lines.push(`data: ${line}`);
  }
  return `${lines.join("\n")}\n\n`;
}

function replaySse(res, fixture, delayMs) {
  res.writeHead(fixture.responseStatus, {
    "content-type": "text/event-stream; charset=utf-8",
    "cache-control": "no-cache",
    connection: "keep-alive",
    ...sanitizeHeaders(fixture.responseHeaders),
  });

  const events = Array.isArray(fixture.responseEvents) ? fixture.responseEvents : [];
  let index = 0;
  const writeNext = () => {
    if (index >= events.length) {
      res.end();
      return;
    }
    const event = events[index];
    index += 1;
    res.write(formatSseEvent(event));
    setTimeout(writeNext, Number(event.delay_ms ?? delayMs));
  };
  writeNext();
}

function serveFixture(res, fixture, delayMs) {
  if (Array.isArray(fixture.responseEvents)) {
    replaySse(res, fixture, delayMs);
    return;
  }
  writeJson(res, fixture.responseStatus, fixture.responseBody ?? null, fixture.responseHeaders);
}

function createMockLegacyServer(options = {}) {
  const fixtureRoot = options.fixtureRoot || process.env.FIXTURE_ROOT || DEFAULT_FIXTURE_ROOT;
  const delayMs = Number(options.sseDelayMs || process.env.SSE_DELAY_MS || DEFAULT_SSE_DELAY_MS);
  const logger = options.logger || console;

  return http.createServer((req, res) => {
    const url = new URL(req.url || "/", "http://mock-legacy.local");
    if (url.pathname === "/__health") {
      writeJson(res, 200, { ok: true, data: { service: "mock-legacy" } });
      return;
    }

    let fixtures;
    try {
      fixtures = loadFixtures(fixtureRoot);
    } catch (error) {
      logger.error(error);
      writeJson(res, 500, { ok: false, error: "fixture_load_failed" });
      return;
    }

    const fixture = findFixture(fixtures, req.method, url.pathname);
    if (!fixture) {
      writeJson(res, 501, {
        ok: false,
        error: `mock not captured: ${normalizeMethod(req.method)} ${url.pathname}`,
      });
      return;
    }

    serveFixture(res, fixture, delayMs);
  });
}

function start() {
  const port = Number(process.env.MOCK_LEGACY_PORT || DEFAULT_PORT);
  const server = createMockLegacyServer();
  server.listen(port, "0.0.0.0", () => {
    console.log(`mock-legacy listening on :${port}`);
  });
}

if (require.main === module) {
  start();
}

module.exports = {
  createMockLegacyServer,
  findFixture,
  formatSseEvent,
  loadFixtures,
  pathMatches,
};
