const http = require('node:http');
const fs = require('node:fs');
const { pipeline } = require('node:stream');
const { formatBytes, sendJson, sharedPath } = require('../shared/lib');

const port = 3002;
const host = '127.0.0.1';
const sampleFile = sharedPath('sample-large.txt');

const metrics = {
  readFile: [],
  stream: [],
};

function snapshotMemory() {
  const { rss, heapUsed, external } = process.memoryUsage();
  return { rss, heapUsed, external };
}

function record(mode, before, after, durationMs) {
  metrics[mode].push({
    at: new Date().toISOString(),
    durationMs,
    before,
    after,
    delta: {
      rss: after.rss - before.rss,
      heapUsed: after.heapUsed - before.heapUsed,
      external: after.external - before.external,
    },
  });
  if (metrics[mode].length > 10) metrics[mode].shift();
}

const server = http.createServer((req, res) => {
  if (req.url === '/metrics') {
    return sendJson(res, 200, {
      note: 'delta 仅用于体会 readFile 与 stream 在内存表现上的差别，非严格 benchmark。',
      latest: {
        readFile: metrics.readFile.at(-1) || null,
        stream: metrics.stream.at(-1) || null,
      },
      pretty: {
        readFileRssDelta: metrics.readFile.at(-1)
          ? formatBytes(metrics.readFile.at(-1).delta.rss)
          : null,
        streamRssDelta: metrics.stream.at(-1)
          ? formatBytes(metrics.stream.at(-1).delta.rss)
          : null,
      },
    });
  }

  if (req.url === '/readFile') {
    const start = Date.now();
    const before = snapshotMemory();
    return fs.readFile(sampleFile, (err, data) => {
      const after = snapshotMemory();
      record('readFile', before, after, Date.now() - start);
      if (err) return sendJson(res, 500, { error: err.message });
      res.writeHead(200, {
        'content-type': 'text/plain; charset=utf-8',
        'content-length': data.length,
        'x-demo-mode': 'readFile',
      });
      res.end(data);
    });
  }

  if (req.url === '/stream') {
    const start = Date.now();
    const before = snapshotMemory();
    res.writeHead(200, {
      'content-type': 'text/plain; charset=utf-8',
      'x-demo-mode': 'stream',
    });
    return pipeline(fs.createReadStream(sampleFile), res, (err) => {
      const after = snapshotMemory();
      record('stream', before, after, Date.now() - start);
      if (err) {
        console.error('[download-compare] stream failed:', err.message);
      }
    });
  }

  sendJson(res, 200, {
    endpoints: ['/readFile', '/stream', '/metrics'],
    sampleFile,
  });
});

server.listen(port, host, () => {
  console.log(`Download compare server: http://${host}:${port}`);
});
