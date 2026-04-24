import { expect, test } from '@playwright/test';
import fs from 'node:fs/promises';
import path from 'node:path';

import { expectEnvelopeOk, loginAs, setRoutingTable } from '../helpers';

test('example harness spec exercises helper utilities', async ({ page }, testInfo) => {
  await loginAs(page, 'staff');
  await page.goto('data:text/html,<main data-testid="ready">ready</main>');
  await expect(page.getByTestId('ready')).toHaveText('ready');

  const routingTablePath = testInfo.outputPath('routing-table.json');
  await fs.writeFile(
    routingTablePath,
    JSON.stringify(
      {
        _comment: 'throwaway routing table for harness example',
        routes: [{ path: '/api/*', target: 'mock' }],
      },
      null,
      2,
    ) + '\n',
  );

  const updated = await setRoutingTable(
    {
      '/api/health': 'django',
      '/api/*': 'mock',
    },
    { routingTablePath },
  );

  expect(updated.routes.map((route) => route.path)).toEqual(['/api/health', '/api/*']);
  expect(path.basename(routingTablePath)).toBe('routing-table.json');

  await expectEnvelopeOk({
    async json() {
      return { ok: true, data: { route: '/api/health' } };
    },
  });
});
