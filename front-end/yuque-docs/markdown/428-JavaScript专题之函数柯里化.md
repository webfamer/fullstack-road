# JavaScript专题之函数柯里化

> 来源：https://www.yuque.com/xiumubai/doc/pl3428uwg0ibvnwd

定义
维基百科中对柯里化 (Currying) 的定义为：
In mathematics and computer science, currying is the technique of translating the evaluation of a function that takes multiple arguments (or a tuple of arguments) into evaluating a sequence of functions, each with a single argument.
翻译成中文：
在数学和计算机科学中，柯里化是一种将使用多个参数的一个函数转换成一系列使用一个参数的函数的技术。
举个例子：

​9912345678910function add(a, b) {    return a + b;}
// 执行 add 函数，一次传入两个参数即可add(1, 2) // 3
// 假设有一个 curry 函数可以做到柯里化var addCurry = curry(add);addCurry(1)(2) // 3用途
我们会讲到如何写出这个 curry 函数，并且会将这个 curry 函数写的很强大，但是在编写之前，我们需要知道柯里化到底有什么用？
举个例子：

​9912345678910111213141516171819202122// 示意而已function ajax(type, url, data) {    var xhr = new XMLHttpRequest();    xhr.open(type, url, true);    xhr.send(data);}
// 虽然 ajax 这个函数非常通用，但在重复调用的时候参数冗余ajax('POST', 'www.test.com', "name=kevin")ajax('POST', 'www.test2.com', "name=kevin")ajax('POST', 'www.test3.com', "name=kevin")
// 利用 curryvar ajaxCurry = curry(ajax);
// 以 POST 类型请求数据var post = ajaxCurry('POST');post('www.test.com', "name=kevin");
// 以 POST 类型请求来自于 www.test.com 的数据var postFromTest = post('www.test.com');postFromTest("name=kevin");想想 jQuery 虽然有 这样通用的方法，但是也有.����这样通用的方法，但是也有.get 和 $.post 的语法糖。(当然 jQuery 底层是否是这样做的，我就没有研究了)。
curry 的这种用途可以理解为：参数复用。本质上是降低通用性，提高适用性。
可是即便如此，是不是依然感觉没什么用呢？
如果我们仅仅是把参数一个一个传进去，意义可能不大，但是如果我们是把柯里化后的函数传给其他函数比如 map 呢？
举个例子：
比如我们有这样一段数据：
var person = [{name: 'kevin'}, {name: 'daisy'}]
如果我们要获取所有的 name 值，我们可以这样做：

​9123var name = person.map(function (item) {    return item.name;})不过如果我们有 curry 函数：

​912345var prop = curry(function (key, obj) {    return obj[key]});
var name = person.map(prop('name'))我们为了获取 name 属性还要再编写一个 prop 函数，是不是又麻烦了些？
但是要注意，prop 函数编写一次后，以后可以多次使用，实际上代码从原本的三行精简成了一行，而且你看代码是不是更加易懂了？
person.map(prop('name')) 就好像直白的告诉你：person 对象遍历(map)获取(prop) name 属性。
是不是感觉有点意思了呢？
第一版
未来我们会接触到更多有关柯里化的应用，不过那是未来的事情了，现在我们该编写这个 curry 函数了。
一个经常会看到的 curry 函数的实现为：

​912345678// 第一版var curry = function (fn) {    var args = [].slice.call(arguments, 1);    return function() {        var newArgs = args.concat([].slice.call(arguments));        return fn.apply(this, newArgs);    };};我们可以这样使用：

​99123456789101112function add(a, b) {    return a + b;}
var addCurry = curry(add, 1, 2);addCurry() // 3//或者var addCurry = curry(add, 1);addCurry(2) // 3//或者var addCurry = curry(add);addCurry(1, 2) // 3已经有柯里化的感觉了，但是还没有达到要求，不过我们可以把这个函数用作辅助函数，帮助我们写真正的 curry 函数。
第二版

我们验证下这个函数：

效果已经达到我们的预期，然而这个 curry 函数的实现好难理解呐……
为了让大家更好的理解这个 curry 函数，我给大家写个极简版的代码：

大家先从理解这个 curry 函数开始。
当执行 fn1() 时，函数返回：

当执行 fn1()() 时，函数返回：

当执行 fn1()()() 时，函数返回：

当执行 fn1()()()() 时，因为此时 length > 2 为 false，所以执行 fn()：

再回到真正的 curry 函数，我们以下面的例子为例：

当执行 fn1("a", "b") 时：

​9912345678910fn1("a", "b")// 相当于curry(fn0)("a", "b")// 相当于curry(sub_curry(fn0, "a", "b"))// 相当于// 注意 ... 只是一个示意，表示该函数执行时传入的参数会作为 fn0 后面的参数传入curry(function(...){    return fn0("a", "b", ...)})当执行 fn1("a", "b")("c") 时，函数返回：

​991234567891011curry(sub_curry(function(...){    return fn0("a", "b", ...)}), "c")// 相当于curry(function(...){    return (function(...) {return fn0("a", "b", ...)})("c")})// 相当于curry(function(...){     return fn0("a", "b", "c", ...)})当执行 fn1("a", "b")("c")("d") 时，此时 arguments.length < length 为 false ，执行 fn(arguments)，相当于：

​912345(function(...){    return fn0("a", "b", "c", ...)})("d")// 相当于fn0("a", "b", "c", "d")函数执行结束。
所以，其实整段代码又很好理解：
sub_curry 的作用就是用函数包裹原函数，然后给原函数传入之前的参数，当执行 fn0(...)(...) 的时候，执行包裹函数，返回原函数，然后再调用 sub_curry 再包裹原函数，然后将新的参数混合旧的参数再传入原函数，直到函数参数的数目达到要求为止。
如果要明白 curry 函数的运行原理，大家还是要动手写一遍，尝试着分析执行步骤。
更易懂的实现
当然了，如果你觉得还是无法理解，你可以选择下面这种实现方式，可以实现同样的效果：

​99123456789101112131415161718192021222324252627282930313233343536function curry(fn, args) {    var length = fn.length;
    args = args || [];
    return function() {
        var _args = args.slice(0),
            arg, i;
        for (i = 0; i < arguments.length; i++) {
            arg = arguments[i];
            _args.push(arg);
        }        if (_args.length < length) {            return curry.call(this, fn, _args);        }        else {            return fn.apply(this, _args);        }    }}

var fn = curry(function(a, b, c) {    console.log([a, b, c]);});
fn("a", "b", "c") // ["a", "b", "c"]fn("a", "b")("c") // ["a", "b", "c"]fn("a")("b")("c") // ["a", "b", "c"]fn("a")("b", "c") // ["a", "b", "c"]或许大家觉得这种方式更好理解，又能实现一样的效果，为什么不直接就讲这种呢？
因为想给大家介绍各种实现的方法嘛，不能因为难以理解就不给大家介绍呐~
第三版
curry 函数写到这里其实已经很完善了，但是注意这个函数的传参顺序必须是从左到右，根据形参的顺序依次传入，如果我不想根据这个顺序传呢？
我们可以创建一个占位符，比如这样：

​912345var fn = curry(function(a, b, c) {    console.log([a, b, c]);});
fn("a", _, "c")("b") // ["a", "b", "c"]我们直接看第三版的代码：

​Plain TextCopy994546474849505152535455565758596061626364656667686970// 第三版                _args.push(arg);            }
        }        if (_holes.length || _args.length < length) {            return curry.call(this, fn, _args, _holes);        }        else {            return fn.apply(this, _args);        }    }}
var _ = {};
var fn = curry(function(a, b, c, d, e) {    console.log([a, b, c, d, e]);});
// 验证 输出全部都是 [1, 2, 3, 4, 5]fn(1, 2, 3, 4, 5);fn(_, 2, 3, 4, 5)(1);fn(1, _, 3, 4, 5)(2);fn(1, _, 3)(_, 4)(2)(5);fn(1, _, _, 4)(_, 3)(2)(5);fn(_, 2)(_, _, 4)(1)(3)(5)写在最后
至此，我们已经实现了一个强大的 curry 函数，可是这个 curry 函数符合柯里化的定义吗？柯里化可是将一个多参数的函数转换成多个单参数的函数，但是现在我们不仅可以传入一个参数，还可以一次传入两个参数，甚至更多参数……这看起来更像一个柯里化 (curry) 和偏函数 (partial application) 的综合应用，可是什么又是偏函数呢？
