const { fib } = require('./fib');

const start = Date.now();
let tick = 0;

const interval = setInterval(() => {
  tick += 1;
  const elapsed = Date.now() - start;
  console.log(`[blocking] timer tick=${tick}, elapsed=${elapsed}ms`);
  if (tick >= 5) clearInterval(interval);
}, 100);

console.log('[blocking] starting CPU heavy fib(43)...');
const result = fib(43);
console.log(`[blocking] fib(43)=${result}, total=${Date.now() - start}ms`);
