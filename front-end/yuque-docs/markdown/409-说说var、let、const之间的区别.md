# 说说var、let、const之间的区别

> 来源：https://www.yuque.com/xiumubai/doc/nlzsrbf7584pe8du

一、var

在ES5中，顶层对象的属性和全局变量是等价的，用var声明的变量既是全局变量，也是顶层变量

注意：顶层对象，在浏览器环境指的是window对象，在 Node 指的是global对象

​912var a = 10;console.log(window.a) // 10
使用var声明的变量存在变量提升的情况

​912console.log(a) // undefinedvar a = 20
在编译阶段，编译器会将其变成以下执行

​9123var aconsole.log(a)a = 20
使用var，我们能够对一个变量进行多次声明，后面声明的变量会覆盖前面的变量声明

​9123var a = 20 var a = 30console.log(a) // 30
在函数中使用使用var声明变量时候，该变量是局部的

​9123456var a = 20function change(){    var a = 30}change()console.log(a) // 20
而如果在函数内不使用var，该变量是全局的

​9123456var a = 20function change(){   a = 30}change()console.log(a) // 30
二、let

let是ES6新增的命令，用来声明变量

用法类似于var，但是所声明的变量，只在let命令所在的代码块内有效

​91234{    let a = 20}console.log(a) // ReferenceError: a is not defined.
不存在变量提升

​912console.log(a) // 报错ReferenceErrorlet a = 2
这表示在声明它之前，变量a是不存在的，这时如果用到它，就会抛出一个错误

只要块级作用域内存在let命令，这个区域就不再受外部影响

使用let声明变量前，该变量都不可用，也就是大家常说的“暂时性死区”

最后，let不允许在相同作用域中重复声明

注意的是相同作用域，下面这种情况是不会报错的

因此，我们不能在函数内部重新声明参数

三、const

const声明一个只读的常量，一旦声明，常量的值就不能改变

这意味着，const一旦声明变量，就必须立即初始化，不能留到以后赋值

如果之前用var或let声明过变量，再用const声明同样会报错

const实际上保证的并不是变量的值不得改动，而是变量指向的那个内存地址所保存的数据不得改动

对于简单类型的数据，值就保存在变量指向的那个内存地址，因此等同于常量

对于复杂类型的数据，变量指向的内存地址，保存的只是一个指向实际数据的指针，const只能保证这个指针是固定的，并不能确保改变量的结构不变

其它情况，const与let一致

四、区别

var、let、const三者区别可以围绕下面五点展开：

●变量提升
●暂时性死区
●块级作用域
●重复声明
●修改声明的变量
●使用

变量提升

var声明的变量存在变量提升，即变量可以在声明之前调用，值为undefined

let和const不存在变量提升，即它们所声明的变量一定要在声明后使用，否则报错

暂时性死区

var不存在暂时性死区

let和const存在暂时性死区，只有等到声明变量的那一行代码出现，才可以获取和使用该变量

​991234567891011// varconsole.log(a)  // undefinedvar a = 10
// letconsole.log(b)  // Cannot access 'b' before initializationlet b = 10
// constconsole.log(c)  // Cannot access 'c' before initializationconst c = 10
块级作用域

var不存在块级作用域

let和const存在块级作用域

​991234567891011121314151617// var{    var a = 20}console.log(a)  // 20
// let{    let b = 20}console.log(b)  // Uncaught ReferenceError: b is not defined
// const{    const c = 20}console.log(c)  // Uncaught ReferenceError: c is not defined
重复声明

var允许重复声明变量

let和const在同一作用域不允许重复声明变量

​JavaScriptRun CodeCopy991234567891011// varvar a = 10var a = 20 // 20
// letlet b = 10let b = 20 // Identifier 'b' has already been declared
// constconst c = 10const c = 20 // Identifier 'c' has already been declared
修改声明的变量

var和let可以

const声明一个只读的常量。一旦声明，常量的值就不能改变

​JavaScriptRun CodeCopy991234567891011121314// varvar a = 10a = 20console.log(a)  // 20
//letlet b = 10b = 20console.log(b)  // 20
// constconst c = 10c = 20console.log(c) // Uncaught TypeError: Assignment to constant variable使用
能用const的情况尽量使用const，其他情况下大多数使用let，避免使用var
参考文献
●[https://es6.ruanyifeng.com/](https://es6.ruanyifeng.com/)
