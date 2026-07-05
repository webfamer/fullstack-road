import cjsLib from './cjs-lib.cjs';
import describe, { formatRole } from './esm-lib.mjs';

console.log(cjsLib.formatName('Grace'));
console.log(formatRole('backend'));
console.log(describe('Grace', 'backend'));
