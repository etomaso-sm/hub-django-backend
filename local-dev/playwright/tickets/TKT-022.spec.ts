import { expect, test } from '@playwright/test';

import { expectEnvelopeOk, loginAs } from '../helpers';

const caddyBase = process.env.TKT022_API_BASE || 'http://localhost:8080';

test('normal user can hit authenticated smoke endpoint through frontend api.js', async ({ page }) => {
  await loginAs(page, 'normal');
  await page.goto('/');

  const body = await page.evaluate(async (apiBase) => {
    const normalizedBase = apiBase.endsWith('/') ? apiBase.slice(0, -1) : apiBase;
    const source = await fetch('/src/lib/api.js').then((response) => response.text());
    const patched = source
      .replace(/var API_BASE = [^;]+;/, `var API_BASE = '${normalizedBase}/api';`)
      .replace('function get(path, params) {', 'export function get(path, params) {');
    const blobUrl = URL.createObjectURL(new Blob([patched], { type: 'text/javascript' }));

    try {
      const api = (await import(blobUrl)) as { get(path: string): Promise<unknown> };
      return await api.get('/_smoke/ping');
    } finally {
      URL.revokeObjectURL(blobUrl);
    }
  }, caddyBase);

  await expectEnvelopeOk({
    async json() {
      return body;
    },
  });
  expect(body).toMatchObject({
    ok: true,
    data: {
      pong: true,
      user_email: 'normal@local.test',
    },
  });
});
