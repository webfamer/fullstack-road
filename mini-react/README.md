# Mini React：面试讲解版

这个目录放了一个零依赖、浏览器直接打开就能跑的最小 React 实现，重点不是功能完整，而是把下面这条链路讲清楚：

`JSX/虚拟 DOM -> Fiber 调度 -> current/workInProgress 双树 -> reconcile -> commit DOM`

## 怎么打开

直接用浏览器打开 [index.html](/Users/xsz/project/front-ai/interview/mini-react/index.html)。

如果你想本地起服务，也可以在这个目录执行：

```bash
python3 -m http.server 8080
```

然后访问 `http://localhost:8080/mini-react/`。

## 文件说明

- [mini-react.js](/Users/xsz/project/front-ai/interview/mini-react/mini-react.js)：核心实现
- [app.js](/Users/xsz/project/front-ai/interview/mini-react/app.js)：示例组件和更新入口
- [usage-examples.js](/Users/xsz/project/front-ai/interview/mini-react/usage-examples.js)：单独整理出来的调用示例
- [index.html](/Users/xsz/project/front-ai/interview/mini-react/index.html)：页面和日志面板

## 最小调用例子

```js
import { createElement, render } from "./mini-react.js";

function Hello(props) {
  return createElement("h1", null, "hello ", props.name);
}

const app = createElement(
  "div",
  { id: "app-shell" },
  createElement(Hello, { name: "fiber" }),
  createElement("p", null, "这就是一个最小调用")
);

render(app, document.getElementById("root"));
```

这段里可以顺着讲：

- `createElement()` 负责生成虚拟 DOM
- `Hello` 是函数组件，本质上就是 `props => element`
- `render()` 不会立刻递归改 DOM，而是先创建 `wipRoot`，再交给 Fiber work loop

## 更新调用例子

```js
let count = 1;

function App() {
  return createElement(
    "div",
    null,
    createElement("h2", null, "count: ", String(count)),
    createElement(
      "button",
      {
        onClick: () => {
          count += 1;
          render(createElement(App, null), document.getElementById("root"));
        },
      },
      "加一"
    )
  );
}

render(createElement(App, null), document.getElementById("root"));
```

这里的重点是：

- 每次点击都会重新生成一棵新的虚拟 DOM 树
- React 风格的框架不会直接就地改旧树，而是新建 `workInProgress`
- 新树和旧树通过 `alternate` 关联，然后在 reconcile 阶段比较差异

## 你可以按这个顺序讲

1. `createElement`
把 JSX 背后的 UI 先变成普通 JS 对象，也就是虚拟 DOM。

2. `render`
不会马上改真实 DOM，而是先创建 `wipRoot`。
这里的 `alternate: currentRoot` 就是双树的连接点。

3. `workLoop`
通过 `requestIdleCallback` 模拟 React 的调度器。一次只做一点工作，浏览器空闲再继续。

4. `performUnitOfWork`
每个 Fiber 节点都是一个工作单元，顺序是：
`child -> sibling -> parent.sibling`
这相当于把递归树遍历改造成可以暂停和恢复的链式遍历。

5. `reconcileChildren`
拿新 element 和旧 fiber 比较。
- 同类型：复用 DOM，打 `UPDATE`
- 新节点：打 `PLACEMENT`
- 旧节点消失：打 `DELETION`

6. `commitRoot`
render 阶段只计算，不操作 DOM。
等整棵 workInProgress 树构建完成后，再统一提交到真实 DOM。

## 面试速讲稿

你可以直接这样说：

> React 里 JSX 最后会变成虚拟 DOM 对象树。更新发生时，React 不会直接改真实 DOM，而是基于当前屏幕上的 current Fiber 树，再创建一棵 workInProgress 树。render 阶段会在这棵新树上做 reconcile，对比新旧节点，标记 placement、update、deletion。Fiber 的意义是把原来不可中断的递归 diff，拆成一个个可中断的工作单元，调度器可以分片执行。等 render 阶段全部算完，再进入 commit 阶段，把 effect 一次性提交到真实 DOM，最后让 workInProgress 变成新的 current 树。

## 代码里最值得看的点

- `render()`：创建 `wipRoot`
- `workLoop()`：调度
- `performUnitOfWork()`：Fiber 遍历
- `reconcileChildren()`：diff + 打 effectTag
- `commitRoot()` / `commitWork()`：提交 DOM

## 这个版本故意省略了什么

- Hooks 链表
- 优先级 lanes
- 完整事件系统
- Fragment / Portal / Context
- 更复杂的 diff 策略

但用来理解面试里最常问的“虚拟 DOM、Fiber、双树、render/commit”已经够用了。
