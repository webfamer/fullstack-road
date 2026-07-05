const { parentPort, workerData } = require('node:worker_threads');
const { fib } = require('./fib');

const result = fib(workerData.n);
parentPort.postMessage({ n: workerData.n, result });
