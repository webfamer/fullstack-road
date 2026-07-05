# JavaScript手写题大全总结

> 来源：https://www.yuque.com/xiumubai/doc/vmigk7ddqwwerg5g

手写forEach
​99123456789101112131415let family = ['jim', 'tom', 'jack', 'kim']Array.prototype.myforEach= function(func) {  if (this === null) {      throw new TypeError('Array.prototype.reduce called on null or undefined');  }  if (typeof func !== 'function') {      throw new TypeError(func + ' is not a function');  }  let arr = this;  for (let i = 0; i < arr.length; i++) {    func(arr[i], i, arr)  }}family.forEach((item, index, arr) => {arr[index] = `hello ${item}`}) // ["hello jim", "hello tom", "hello jack", "hello kim"]family.myforEach((item, index, arr) => {arr[index] = `${item}!`}) // ["hello jim!", "hello tom!", "hello jack!", "hello kim!"]
手写map
​99123456789101112131415161718let family = ['jim', 'tom', 'jack', 'kim']Array.prototype.myMap= function(func) {  if (this === null) {      throw new TypeError('Array.prototype.reduce called on null or undefined');  }  if (typeof func !== 'function') {      throw new TypeError(func + ' is not a function');  }  let arr = this;  console.log(arr)  let newArr = [];  for (let i = 0; i < arr.length; i++) {    newArr.push(func(arr[i], i, arr))  }  return newArr;}let  arr1 = family.map((item, index, arr) => {return `hello ${item}`})  // ["hello jim", "hello tom", "hello jack", "hello kim"]let  arr2 = family.myMap((item, index, arr) => {return `hello ${item}`})  // ["hello jim", "hello tom", "hello jack", "hello kim"]
手写filer
​9912345678910111213141516171819let family = ['jim', 'tom', 'jack', 'kim']Array.prototype.myFilter= function(func) {  if (this === null) {      throw new TypeError('Array.prototype.reduce called on null or undefined');  }  if (typeof func !== 'function') {      throw new TypeError(func + ' is not a function');  }  let arr = this;  let newArr = [];  for (let i = 0; i < arr.length; i++) {    if (func(arr[i], i, arr)) {      newArr.push(arr[i])    }  }  return newArr;}let arr1 = family.filter((item, index, arr) => { return index !== 2}) // ['jim', 'tom', 'kim']let arr2 = family.myFilter((item, index, arr) => { return index !== 2}) // ['jim', 'tom', 'kim']
手写some
​99123456789101112131415161718192021222324252627282930313233343536let family = ['jim', 'tom', 'jack', 'kim']Array.prototype.mySome= function(func) {  if (this === null) {      throw new TypeError('Array.prototype.reduce called on null or undefined');  }  if (typeof func !== 'function') {      throw new TypeError(func + ' is not a function');  }  let arr = this;  for (let i = 0; i < arr.length; i++) {    if (func(arr[i], i, arr)) {      return true    }  }  return false;}family.some((item, index, arr) => { return item === 'bim'}) // truefamily.mySome((item, index, arr) => { return item === 'bim'}) // true// everyArray.prototype.myEvery= function(func) {  if (this === null) {      throw new TypeError('Array.prototype.reduce called on null or undefined');  }  if (typeof func !== 'function') {      throw new TypeError(func + ' is not a function');  }  let arr = this;  for (let i = 0; i < arr.length; i++) {    if (!func(arr[i], i, arr)) {      return false;    }  }  return true;}family.every((item, index, arr) => { return item === 'bim'}) // falsefamily.myEvery((item, index, arr) => { return item === 'bim'}) // false
手写find
​99123456789101112131415161718192021222324252627282930313233343536let family = ['jim', 'tom', 'jack', 'kim']Array.prototype.myFind= function(func) {  if (this === null) {      throw new TypeError('Array.prototype.reduce called on null or undefined');  }  if (typeof func !== 'function') {      throw new TypeError(func + ' is not a function');  }  let arr = this;  for (let i = 0; i < arr.length; i++) {    if (func(arr[i], i, arr)) {      return arr[i]    }  }  return undefined;}let name1 = family.find((item, index, arr) => { return item === 'kim'}) // kimlet name2 = family.myFind((item, index, arr) => { return item === 'kim'})  // kim// findIndexArray.prototype.myFindIndex= function(func) {  if (this === null) {      throw new TypeError('Array.prototype.reduce called on null or undefined');  }  if (typeof func !== 'function') {      throw new TypeError(func + ' is not a function');  }  let arr = this;  for (let i = 0; i < arr.length; i++) {    if (func(arr[i], i, arr)) {      return i    }  }  return -1;}let num1 = family.findIndex((item, index, arr) => { return item === 'kim'}) // 3let num2 = family.myFindIndex((item, index, arr) => { return item === 'kim'})  // 3
手写reduce
​99123456789101112131415161718192021222324252627282930313233343536let family = ['jim', 'tom', 'jack', 'kim']Array.prototype.myReduce = function(func, initialValue) {  if (this === null) {      throw new TypeError('Array.prototype.reduce called on null or undefined');  }  if (typeof func !== 'function') {      throw new TypeError(func + ' is not a function');  }  let arr = this;  let prev = initialValue || arr[0]  let len = initialValue ? arr.length : arr.length - 1  for (let i = 0; i < len; i++) {    let cur = initialValue ? arr[i] : arr[i + 1]    prev = func(prev, cur, i, arr)  }  return prev;}let arr1 = family.reduce((prev, cur, index, arr) => { return `${prev}-${cur}`}) // jim-tom-jack-kimlet arr2 = family.myReduce((prev, cur, index, arr) => { return `${prev}-${cur}`}) // jim-tom-jack-kim// reduceRightArray.prototype.myReduceRight = function(func, initialValue) {  if (this === null) {      throw new TypeError('Array.prototype.reduce called on null or undefined');  }  if (typeof func !== 'function') {      throw new TypeError(func + ' is not a function');  }  let arr = this;  let prev = initialValue || arr[arr.length - 1]  let num = initialValue ? -1 : 0  for (let i = arr.length - 1; i > num; i--) {    let cur = initialValue ? arr[i] : arr[i - 1]    prev = func(prev, cur, i, arr)  }  return prev;}
手写Array.from
​912345Array.myFrom = function (el) {  return Array.apply(this, el);}var arrLike = {length: 4, 2: "foo" };var arr = Array.from( arrLike ); //  [undefined, undefined, "foo", undefined]
手写对象属性迭代器
​991234567891011121314151617181920212223242526var obj = {  name: 'AAA',  age: 23,  address: '广州'}Object.defineProperty(obj, Symbol.iterator, {  writable: false,  enumerable: false,  configurable: true,  value: function() {    var self = this;    var index = 0;    var keys = Object.keys(self);    return {      next: function() {        return {          value: self[keys[index++]],          done: index > keys.length        }      }    }  }})for (const val of obj) {  console.log(`属性值为：${val}`);}

手写call
​99123456789101112131415161718192021222324252627282930313233343536Function.prototype.myCall = function (context) {  if (typeof this !== "function") {    throw new Error("Error");  }  context = context || window   // context是第一个参数，作为this将要指向的对象，当传入null或者undefined时指向window  context.fn = this             // 这里的this代表调用myCall的函数，向context对象添加这个函数,其实是改变this指向  var args = [];  for(var i = 1, len = arguments.length; i < len; i++) {     args.push('arguments[' + i + ']'); // 获取第二个到最后一个参数,将类数组对象转成数组  }  var result = eval('context.fn(' + args +')'); // 传入参数并执行函数  delete context.fn                           // 从对象中删除这个属性  return result;                              // 返回结果}// es6Function.prototype.yourCall = function (context) {  if (typeof this !== "function") {     throw new Error("Error");  }  context = context || window;   context.fn = this;  let args = [...arguments].slice(1);  let result = context.fn(...args);  delete context.fn  return result;}
var color = 'blue'let colors = {  color: 'red'}
function box(width, height) {  console.log(width)  console.log(height)  console.log(this.color)
手写apply
​99123456789101112131415161718192021222324252627282930313233343536Function.prototype.myApply = function (context, arr) {  if (typeof this !== "function") {    throw new Error("Error");  }  context = context || window;  context.fn = this;  var result;  if (!arr) {    result = context.fn();  }  else {    var args = [];    for (var i = 0, len = arr.length; i < len; i++) {       args.push('arr[' + i + ']');    }    result = eval('context.fn(' + arr + ')')  }  delete context.fn  return result;}// es6Function.prototype.yourApply = function (context, arr) {    if (typeof this !== "function") {      throw new Error("Error");    }    context = context || window;     context.fn = this;    let result;    if (!arr) {        result = context.fn();    } else {        result = context.fn(...arr);    }    delete context.fn    return result;}
手写bind
​991234567891011121314151617181920212223242526272829303132333435Function.prototype.myBind = function (context) {    if (typeof this !== "function") {      throw new Error("Error");    }     let self = this;    let args = [...arguments].slice(1);    let newFuc = function () {};    let resultFuc = function () {        var bindArgs = [...arguments].slice();        // 当作为构造函数时，this 指向实例，此时结果为 true，将绑定函数的 this 指向该实例，可以让实例获得来自绑定函数的值        // 当作为普通函数时，this 指向 window，此时结果为 false，将绑定函数的 this 指向 context        return self.apply(this instanceof newFuc ? this : context, args.concat(bindArgs));    }    // 修改返回函数的 prototype 为绑定函数的 prototype，实例就可以继承绑定函数的原型中的值    newFuc.prototype = self.prototype;    resultFuc.prototype = new newFuc();    return resultFuc;}let colors = {  color: 'red'}
function box(width, height) {  this.length = 20  console.log(width)  console.log(height)  console.log(this.color)}box.prototype.price = 666
let mybox = box.myBind(colors, 200)mybox(300)  // 200, 300, red mybox作为普通函数，this指向了colorslet yourBox = new mybox(300) // 200, 300, undefinedconsole.log(yourBox.length, yourBox.price) // 20 ,600 mybox作为构造函数，this指向了实例yourBox
手写instanceof

手写Object.create()

手写new

手写Object.assin()

手写深拷贝

手写JSON.stringify、JSON.parse

手写promise

手写co

手写async/awai

手写AJAX

手写JSONP

手写双向绑定

手写柯里化函数

手写防抖函数

手写节流函数
手写事件委托

手写AOP

手写 ES6 的 class 语法

手写模版引擎
手写EventEmitter

实现简单路由

手写图片懒加载

手写图片预加载

手写分时函数

手写拖拽

手写localstorge

手写setInterval方法

手写sleep函数

手写GetQueryString

手写flatten
​99123456789101112131415161718192021222324252627282930313233343536  function flatten1(arr) {    return arr.join(',').split(',').map(function(item) {      return Number(item);    })  }  function flatten2(arr) {    var newArr = [];    arr.map(item => {      if(Array.isArray(item)){        newArr.push(...flatten2(item))      } else {        newArr.push(item)      }    })    return newArr  }
  function flatten3(arr) {    let stack = [...arr].reverse()    let newArr = []    while(stack.length){      let o = stack.pop()      if(Array.isArray(o)){        stack.push(...o.reverse())      } else {        newArr.push(o)      }    }    return newArr  }  function flatten4(arr) {    while(arr.some(item=>Array.isArray(item))) {      arr = [].concat(...arr);    }    return arr;  }
手写发布订阅

​99123456789101112131415161718192021222324252627282930313233class Subject{    constructor(){        this.observers = [];    }    addObserver(observer){        this.observers.push(observer);    }    removeObserver(observer){        var index = this.observers.indexOf(observer);        if(index>-1){            this.observers.splice(index,1);        }    }    notify(){        this.observers.forEach(function(observer){            observer.update();        })    }}
class Observer{    constructor(name){        this.name = name;    }    update(){        console.log(this.name+'update...');    }}
var subject = new Subject();subject.addObserver(new Observer('主题一'));subject.addObserver(new Observer('主题二'));subject.notify();

Promise.all并发控制

​99123456789101112131415161718192021222324252627282930313233343536function promiseall(promises) {  return new Promise(resolve => {    let result = [];    let flag = 0;    let taskQueue = promises.slice(0, 3); //任务队列，初始为最大并发数3    let others = promises.slice(3); //排队的任务
    taskQueue.forEach((promise, i) => {      singleTaskRun(promise, i);    });
    let i = 3; //新的任务从索引3开始    function next() {      if (others.length === 0) {        return;      }      const newTask = others.shift();      singleTaskRun(newTask, i++);    }
    function singleTaskRun(promise, i) {      promise        .then(res => {          check();          result[i] = res;          next();        })        .catch(err => {          check();          result[i] = err;          next();        });    }    function check() {      flag++;      if (flag === promises.length) {
Object.is
​991234567891011if (!Object.is) { Object.is = function(x, y) {   if (x === y) { // Steps 1-5, 7-10     // 针对 +0不等于-0     return x !== 0 || 1 / x === 1 / y;   } else {     // 针对 NaN等于NaN     return x !== x && y !== y;   } };}
手写二叉树

​99123456789101112131415161718192021222324252627282930313233343536    //定义插入对象    function BST(){        this.root = null;        this.insert = insert;        this.show = ()=>{           console.log(this.root);        }    }    function insert(data) {        //实例化Node对象        let n = new Node(data,null,null);        //如果不存在节点，则此节点是根节点        if(this.root == null){            this.root = n;        }else{            //存在根节点时，定义current白能量等于根节点            let current = this.root;            let parent;            while(current){                parent = current;                //当插入的值小于根节点的值时，将值作为左节点插入                if(data<current.data) {                    current = current.left;                    if(current == null) {                        parent.left = n;                        break;                    }                }else{                    current = current.right;                    if(current == null){                        parent.right = n;                        break;                    }                }            }         }
Layzi类

​99123456789101112131415161718192021222324252627282930313233343536  function _LazyMan(name){    this.nama = name;    this.queue = [];    this.queue.push(() => {        console.log("Hi! This is " + name + "!");        this.next();    })    setTimeout(()=>{        this.next()    },0)  }    _LazyMan.prototype.eat = function(name){    this.queue.push(() =>{        console.log("Eat " + name + "~");        this.next()    })    return this;  }
  _LazyMan.prototype.next = function(){    var fn = this.queue.shift();    fn && fn();  }
  _LazyMan.prototype.sleep = function(time){    this.queue.push(() =>{        setTimeout(() => {            console.log("Wake up after " + time + "s!");            this.next()        },time * 1000)    })    return this;  }
  _LazyMan.prototype.sleepFirst = function(time){
金钱千分位

​JavaScriptRun CodeCopy9912345678910111213141516171819202122232425function formatRegExp1(number) {    var pattern = /(?=(\B\d{3})+\.)/g    return number.toFixed(2).toString().replace(pattern, ',')}
function formatRegExp2(number) {    var pattern = /(\d)(?=(?:\d{3})+\.)/g    return number.toFixed(2).toString().replace(pattern, '$1,')}
function format(number) {    number = number.toFixed(2).toString()    var dotIndex = number.indexOf('.')    var part = number.substring(0, dotIndex)    var flag = 0    var result = ''    for (var i = part.length - 1; i >= 0; i--) {        result = part[i] + result        if (i !== 0 && ++flag === 3) {            result = ',' + result            flag = 0        }    }    return result + number.substring(dotIndex)}
模板字符串
​JavaScriptRun CodeCopy9123456function template(html, obj) {  return html.replace(/{{(.*?)}}/g, function(match, key) {    return obj[key.trim()];  });}template('{{name}}很厉name害，才{{ age }}岁', { name: 'jawil', age: '15' });手写toFixed
​JavaScriptRun CodeCopy9912345678910111213141516171819202122function toFiexd(num, d){  num * = Math.pow(10, d)  num = Math.round(num)  return num /  Math.pow(10, d)}
function toFixed(value, digits) {  // 返回四舍五入后的字符串  const temp = value * Math.pow(10, digits);  let [left, right] = String(temp).split('.');
  if (Number(right) >= 5) {    left = Number(left) + 1;  }
  const leftArr = String(left).split('');  leftArr.splice(-digits, 0, '.');  return leftArr.join('');}
console.log('Wrong', (4.05).toFixed(1)); // 内置函数有精度问题console.log('Right', toFixed(4.05, 1)); // 输出 '4.1'
