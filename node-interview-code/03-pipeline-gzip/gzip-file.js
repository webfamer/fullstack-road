const fs = require('node:fs');
const zlib = require('node:zlib');
const { pipelineAsync, sharedPath } = require('../shared/lib');

async function main() {
  const source = sharedPath('sample-large.txt');
  const target = sharedPath('sample-large.txt.gz');

  const sourceStat = fs.statSync(source);
  console.log(`Compressing ${source} (${sourceStat.size} bytes) -> ${target}`);

  await pipelineAsync(
    fs.createReadStream(source),
    zlib.createGzip(),
    fs.createWriteStream(target)
  );

  const targetStat = fs.statSync(target);
  console.log(`Done. Output size: ${targetStat.size} bytes`);
}

main().catch((err) => {
  console.error('[gzip] failed:', err);
  process.exitCode = 1;
});
