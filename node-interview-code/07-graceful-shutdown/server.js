const http = require('node:http');
const { sendJson } = require('../shared/lib');

const port = 3004;
const host = '127.0.0.1';
let shuttingDown = false;
const sockets = new Set();

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const server = http.createServer(async (req, res) => {
  if (shuttingDown) {
    res.setHeader('connection', 'close');
    return sendJson(res, 503, { error: 'server is shutting down' });
  }

  if (req.url === '/slow') {
    await sleep(5000);
    return sendJson(res, 200, { ok: true, route: 'slow', waitedMs: 5000 });
  }

  if (req.url === '/health') {
    return sendJson(res, 200, { ok: true, shuttingDown });
  }

  return sendJson(res, 200, { ok: true, route: req.url, pid: process.pid });
});

server.on('connection', (socket) => {
  sockets.add(socket);
  socket.on('close', () => sockets.delete(socket));
});

function shutdown(signal) {
  if (shuttingDown) return;
  shuttingDown = true;
  console.log(`[graceful] received ${signal}, stop accepting new connections`);

  server.close((err) => {
    if (err) {
      console.error('[graceful] close failed:', err);
      process.exitCode = 1;
    }
    console.log('[graceful] all existing requests finished, exiting');
    process.exit();
  });

  setTimeout(() => {
    console.warn('[graceful] force closing remaining sockets');
    for (const socket of sockets) socket.destroy();
  }, 8000).unref();
}

process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));

server.listen(port, host, () => {
  console.log(`[graceful] server listening on http://${host}:${port}, pid=${process.pid}`);
});
