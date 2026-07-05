const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { pipeline } = require('node:stream');
const { sendJson, sharedPath } = require('../shared/lib');

const publicDir = sharedPath('public');
const port = 3001;
const host = '127.0.0.1';

const mimeTypes = {
  '.html': 'text/html; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
};

function safeResolve(publicRoot, requestPath) {
  const pathname = decodeURIComponent(requestPath.split('?')[0]);
  const normalized = pathname === '/' ? '/index.html' : pathname;
  const absolute = path.resolve(publicRoot, `.${normalized}`);
  if (!absolute.startsWith(path.resolve(publicRoot))) return null;
  return absolute;
}

const server = http.createServer((req, res) => {
  const filePath = safeResolve(publicDir, req.url || '/');
  if (!filePath) {
    return sendJson(res, 403, { error: 'forbidden path' });
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      return sendJson(res, 404, { error: 'file not found' });
    }

    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, {
      'content-type': mimeTypes[ext] || 'application/octet-stream',
      'content-length': stats.size,
    });

    pipeline(fs.createReadStream(filePath), res, (pipelineErr) => {
      if (pipelineErr) {
        console.error('[static-server] pipeline failed:', pipelineErr.message);
        if (!res.headersSent) {
          sendJson(res, 500, { error: 'failed to send file' });
        } else {
          res.destroy(pipelineErr);
        }
      }
    });
  });
});

server.listen(port, host, () => {
  console.log(`Static server listening: http://${host}:${port}`);
  console.log(`Try / and /hello.txt`);
});
