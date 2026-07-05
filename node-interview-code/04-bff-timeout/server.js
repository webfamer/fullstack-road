const http = require('node:http');
const { URL } = require('node:url');
const { sendJson } = require('../shared/lib');

const port = 3003;
const host = '127.0.0.1';

function sleep(ms, { signal } = {}) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(resolve, ms);
    if (signal) {
      signal.addEventListener(
        'abort',
        () => {
          clearTimeout(timer);
          reject(new Error('aborted'));
        },
        { once: true }
      );
    }
  });
}

async function fakeUserService() {
  await sleep(200);
  return { id: 1, name: 'Ada', role: 'frontend-to-fullstack' };
}

async function fakeOrdersService(delay, { signal }) {
  await sleep(delay, { signal });
  return [
    { id: 'o-1001', amount: 99, status: 'paid' },
    { id: 'o-1002', amount: 199, status: 'shipping' },
  ];
}

async function withTimeout(task, timeoutMs) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await task(controller.signal);
  } finally {
    clearTimeout(timeout);
  }
}

const server = http.createServer(async (req, res) => {
  const requestUrl = new URL(req.url || '/', `http://${req.headers.host}`);

  if (requestUrl.pathname === '/api/profile') {
    return sendJson(res, 200, await fakeUserService());
  }

  if (requestUrl.pathname === '/api/orders') {
    const delay = Number(requestUrl.searchParams.get('delay') || '500');
    try {
      const data = await withTimeout((signal) => fakeOrdersService(delay, { signal }), 800);
      return sendJson(res, 200, data);
    } catch (err) {
      return sendJson(res, 504, { error: 'orders service timeout', detail: err.message });
    }
  }

  if (requestUrl.pathname === '/bff/dashboard') {
    const ordersDelay = Number(requestUrl.searchParams.get('ordersDelay') || '500');
    const results = await Promise.allSettled([
      fakeUserService(),
      withTimeout((signal) => fakeOrdersService(ordersDelay, { signal }), 800),
    ]);

    const [profileResult, ordersResult] = results;
    return sendJson(res, 200, {
      profile: profileResult.status === 'fulfilled' ? profileResult.value : null,
      orders: ordersResult.status === 'fulfilled' ? ordersResult.value : [],
      warnings: results
        .map((item, index) => ({ index, item }))
        .filter(({ item }) => item.status === 'rejected')
        .map(({ index, item }) => ({
          source: index === 0 ? 'profile' : 'orders',
          reason: item.reason.message,
        })),
    });
  }

  sendJson(res, 200, {
    endpoints: [
      '/api/profile',
      '/api/orders',
      '/api/orders?delay=1200',
      '/bff/dashboard',
      '/bff/dashboard?ordersDelay=1200',
    ],
  });
});

server.listen(port, host, () => {
  console.log(`BFF demo server: http://${host}:${port}`);
});
