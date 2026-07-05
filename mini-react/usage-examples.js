import { createElement, render } from "./mini-react.js";

// 例子 1：最简单的宿主组件渲染
const simpleTree = createElement(
  "section",
  { title: "simple-demo" },
  createElement("h1", null, "Hello Mini React"),
  createElement("p", null, "createElement 先生成虚拟 DOM，再 render")
);

// render(simpleTree, document.getElementById("root"));

// 例子 2：函数组件
function Badge(props) {
  return createElement("strong", null, `[${props.text}]`);
}

function HelloCard(props) {
  return createElement(
    "div",
    { className: "card" },
    createElement("h2", null, "Hi, ", props.name),
    createElement("p", null, "这是一个函数组件"),
    createElement(Badge, { text: "fiber" })
  );
}

// render(createElement(HelloCard, { name: "interview" }), document.getElementById("root"));

// 例子 3：手动触发一次更新，模拟 React setState 后重新 render
let count = 0;

function CounterApp() {
  return createElement(
    "div",
    null,
    createElement("h2", null, "count: ", String(count)),
    createElement(
      "button",
      {
        onClick: () => {
          count += 1;
          render(createElement(CounterApp, null), document.getElementById("root"));
        },
      },
      "add"
    )
  );
}

// render(createElement(CounterApp, null), document.getElementById("root"));

export { simpleTree, Badge, HelloCard, CounterApp };
