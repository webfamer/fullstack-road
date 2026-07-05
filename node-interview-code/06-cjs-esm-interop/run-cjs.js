const cjsLib = require('./cjs-lib.cjs');

async function main() {
  console.log(cjsLib.formatName('Ada'));

  const esmModule = await import('./esm-lib.mjs');
  console.log(esmModule.formatRole('fullstack'));
  console.log(esmModule.default('Ada', 'fullstack'));
}

main().catch((err) => {
  console.error('[interop:cjs] failed:', err);
  process.exitCode = 1;
});
