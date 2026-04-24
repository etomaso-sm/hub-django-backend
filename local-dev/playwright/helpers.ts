import { expect, type APIResponse, type Page } from '@playwright/test';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

type RouteTarget = 'django' | 'mock';
type RoutingPatch = Record<string, RouteTarget>;

type RoutingRoute = {
  path: string;
  target: RouteTarget;
  note?: string;
};

type RoutingTable = {
  _comment?: string;
  routes: RoutingRoute[];
};

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_ROUTING_TABLE = path.resolve(HERE, '..', 'routing-table.json');

function routeSpecificity(routePath: string): number {
  return routePath.replace(/\*$/, '').length;
}

export async function loginAs(page: Page, role: 'normal' | 'staff' | 'superadmin'): Promise<void> {
  await page.addInitScript((selectedRole) => {
    window.localStorage.setItem('hub_test_role', selectedRole);
    const email = selectedRole === 'superadmin' ? 'super@local.test' : `${selectedRole}@local.test`;
    window.localStorage.setItem('hub_user_email', email);
  }, role);
}

export async function setRoutingTable(
  patch: RoutingPatch,
  options: { routingTablePath?: string } = {},
): Promise<RoutingTable> {
  const routingTablePath = options.routingTablePath || DEFAULT_ROUTING_TABLE;
  const raw = await fs.readFile(routingTablePath, 'utf8');
  const table = JSON.parse(raw) as RoutingTable;
  const routeMap = new Map<string, RoutingRoute>();

  for (const route of table.routes || []) {
    routeMap.set(route.path, route);
  }
  for (const [routePath, target] of Object.entries(patch)) {
    routeMap.set(routePath, { path: routePath, target, note: 'set by Playwright harness' });
  }

  table.routes = Array.from(routeMap.values()).sort(
    (a, b) => routeSpecificity(b.path) - routeSpecificity(a.path),
  );
  await fs.writeFile(routingTablePath, `${JSON.stringify(table, null, 2)}\n`);
  return table;
}

export async function expectEnvelopeOk(response: APIResponse | { json(): Promise<unknown> }): Promise<unknown> {
  const body = await response.json();
  expect(body).toMatchObject({ ok: true });
  return body;
}
