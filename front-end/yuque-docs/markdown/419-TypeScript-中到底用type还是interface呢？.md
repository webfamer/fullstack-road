# TypeScript 中到底用type还是interface呢？

> 来源：https://www.yuque.com/xiumubai/doc/vg6npl7o0ghik250

结论
直接说结论，用type一把梭即可，除非你要发布到npm，接下来我一一解释
为什么定义对象都要使用type呢？
如图所示，我鼠标悬浮后，并不知道里面是什么东西
只能获取结果时调出代码提示，或者ctrl + 鼠标左键进入，查看类型定义
那么我用type呢？
![](https://cdn.nlark.com/yuque/0/2023/webp/338969/1702952075283-97014f2e-9e6b-49a6-ba5d-2cace2daf276.webp)
image.png
可以看到，现在鼠标悬浮能直接查看类型定义了
这一点是让我最受不了的，所以直接选择type即可
![](https://cdn.nlark.com/yuque/0/2023/webp/338969/1702952075376-f9370061-0ca3-4f5c-97d0-4627217ea8e4.webp)
image.png
区别
1. 如何继承
先看看interface，通过extends关键字
![](https://cdn.nlark.com/yuque/0/2023/webp/338969/1702952075327-370d61b5-e331-442c-b543-03bdae4fa926.webp)
image.png
type，则通过交叉类型。不过我认为interface好看点
![](https://cdn.nlark.com/yuque/0/2023/webp/338969/1702952075337-dd0f2277-113b-4bb8-b95f-e33eb8c3746c.webp)
image.png
2. 其他特性
当interface重写时
●如果有不同的属性，则会添加；
●如果是相同的属性但是类型不同，则会报错;
这点有好有坏，当你不小心名字重复了，那你就容易出问题
但同时利于扩展，不过没有人会这么写吧？
直接去原来的接口添加属性不行吗？
唯一的场景，就是开发工具库后。别人使用你的工具时，可以为你扩展类型
![](https://cdn.nlark.com/yuque/0/2023/webp/338969/1702952075320-5d65cbdb-5b4f-4b42-8fa3-e490f4468807.webp)
image.png
3. type独有的优势
除了上面的悬浮能查看具体类型外，type还提供了很多的关键字使用，这是interface不具备的
比如in关键字，用来枚举类型
这里我写个删除属性的泛型，和Omit一样的，但是interface不支持
此外还有很多TS特有的关键字，都只能通过type使用，比如infer等
不过这也符合直觉，因为interface就是定义一个类型而已
![](https://cdn.nlark.com/yuque/0/2023/webp/338969/1702952075872-985acf74-474a-4518-8ef7-7a2e1b45416c.webp)
image.png
经过以上探讨，可以得出一个结论：
「平时开发可以都用type」
「发布工具库给别人用时，用interface」
