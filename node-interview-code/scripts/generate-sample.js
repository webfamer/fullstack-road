const fs = require('node:fs');
const path = require('node:path');
const { ensureDir, sharedPath } = require('../shared/lib');

const publicDir = sharedPath('public');
const samplePath = sharedPath('sample-large.txt');

ensureDir(publicDir);

if (!fs.existsSync(path.join(publicDir, 'hello.txt'))) {
  fs.writeFileSync(path.join(publicDir, 'hello.txt'), 'hello from node static server\n');
}

if (!fs.existsSync(path.join(publicDir, 'index.html'))) {
  fs.writeFileSync(
    path.join(publicDir, 'index.html'),
    '<!doctype html><html><body><h1>Node Interview Demo</h1></body></html>\n'
  );
}

if (!fs.existsSync(samplePath)) {
  const line =
    'Node.js stream sample line - use this file to compare readFile and stream memory behavior.\n';
  const targetSize = 20 * 1024 * 1024;
  const fd = fs.openSync(samplePath, 'w');
  let written = 0;
  while (written < targetSize) {
    written += fs.writeSync(fd, line);
  }
  fs.closeSync(fd);
  console.log(`Created sample file: ${samplePath}`);
} else {
  console.log(`Sample file already exists: ${samplePath}`);
}
