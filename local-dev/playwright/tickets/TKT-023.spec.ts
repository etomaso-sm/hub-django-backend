import { expect, test, type Route } from '@playwright/test';

import { expectEnvelopeOk } from '../helpers';

const caddyBase = (process.env.TKT023_API_BASE || 'http://localhost:8080').replace(/\/+$/, '');

function caddyUrlFor(route: Route): string {
  const url = new URL(route.request().url());
  return `${caddyBase}${url.pathname}${url.search}`;
}

async function proxyToCaddy(route: Route): Promise<void> {
  const response = await route.fetch({ url: caddyUrlFor(route) });
  await route.fulfill({ response });
}

test('staff can log in through core auth and see /api/me data in the shell', async ({
  context,
  page,
  request,
}) => {
  const apiLogin = await request.post(`${caddyBase}/api/auth/login`, {
    data: { email: 'staff@local.test' },
  });
  expect(apiLogin.status()).toBe(200);
  const apiLoginBody = (await expectEnvelopeOk(apiLogin)) as {
    data: { email: string; tenant_id: string; url: string };
  };
  expect(apiLoginBody.data).toMatchObject({
    email: 'staff@local.test',
    tenant_id: 'sprint_mode',
    url: '/brief',
  });
  expect(apiLogin.headers()['set-cookie']).toContain('hub_session=');
  expect(apiLogin.headers()['set-cookie']).toContain('hub_context=sprint_mode');

  await page.addInitScript(() => {
    window.localStorage.setItem('hub_onb_done_staff@local.test', '1');
    window.localStorage.setItem('hub_team_tour_done_staff@local.test', '1');
  });

  let submittedLogin = false;
  await page.route('**/api/**', async (route) => {
    const url = new URL(route.request().url());
    const path = url.pathname;

    if (path === '/api/auth/session' && !submittedLogin) {
      await route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({ ok: false, error: 'not authenticated' }),
      });
      return;
    }

    if (path === '/api/auth/login') {
      const response = await route.fetch({ url: caddyUrlFor(route) });
      submittedLogin = true;
      await route.fulfill({ response });
      return;
    }

    if (
      path === '/api/auth/session' ||
      path === '/api/me' ||
      path === '/api/tenants' ||
      path === '/api/hub/list' ||
      path === '/api/hub/current' ||
      path === '/api/hub/switch'
    ) {
      await proxyToCaddy(route);
      return;
    }

    await route.fallback();
  });

  await page.goto('/');
  await expect(page.getByText('Log in')).toBeVisible();

  await page.getByText('Log in').click();
  await expect(page).toHaveURL(/\/$/);
  await expect(page.getByText('Staff User')).toBeVisible({ timeout: 15_000 });

  const me = await page.evaluate(async () => {
    return fetch('/api/me').then((response) => response.json());
  });
  expect(me).toMatchObject({
    ok: true,
    data: {
      email: 'staff@local.test',
      display_name: 'Staff User',
      role: 'staff',
    },
  });

  const cookies = await context.cookies();
  expect(cookies.some((cookie) => cookie.name === 'hub_session')).toBe(true);
  expect(cookies.find((cookie) => cookie.name === 'hub_context')?.value).toBe('sprint_mode');
});
