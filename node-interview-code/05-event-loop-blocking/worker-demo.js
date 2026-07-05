const path = require('node:path');
const { Worker } = require('node:worker_threads');

const start = Date.now();
let tick = 0;

const interval = setInterval(() => {
  tick += 1;
  console.log(`[worker] timer tick=${tick}, elapsed=${Date.now() - start}ms`);
  if (tick >= 5) clearInterval(interval);
}, 100);

console.log('[worker] starting fib(43) in worker thread...');

const worker = new Worker(path.join(__dirname, 'worker-task.js'), {
  workerData: { n: 43 },
});

worker.on('message', (message) => {
  console.log(`[worker] fib(${message.n})=${message.result}, total=${Date.now() - start}ms`);
});

worker.on('error', (err) => {
  console.error('[worker] failed:', err);
  process.exitCode = 1;
});
