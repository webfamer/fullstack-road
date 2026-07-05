const fs = require('node:fs');
const path = require('node:path');
const { pipeline } = require('node:stream');

const rootDir = __dirname;

function sharedPath(...segments) {
  return path.join(rootDir, ...segments);
}

function sendJson(res, statusCode, payload) {
  const body = JSON.stringify(payload, null, 2);
  res.writeHead(statusCode, {
    'content-type': 'application/json; charset=utf-8',
    'content-length': Buffer.byteLength(body),
  });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

function pipelineAsync(...streams) {
  return new Promise((resolve, reject) => {
    pipeline(...streams, (err) => {
      if (err) reject(err);
      else resolve();
    });
  });
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 ** 2) return `${(bytes / 1024).toFixed(2)} KB`;
  if (bytes < 1024 ** 3) return `${(bytes / 1024 ** 2).toFixed(2)} MB`;
  return `${(bytes / 1024 ** 3).toFixed(2)} GB`;
}

module.exports = {
  ensureDir,
  formatBytes,
  pipelineAsync,
  readBody,
  rootDir,
  sendJson,
  sharedPath,
};
