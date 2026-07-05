import { createElement, render, setLogger } from "./mini-react.js";

const logNode = document.getElementById("log");
const root = document.getElementById("root");

function pushLog(message) {
  logNode.textContent += `${message}\n`;
  logNode.scrollTop = logNode.scrollHeight;
}

setLogger(pushLog);

let state = {
  count: 1,
  showTips: true,
};

function CounterCard({ count, showTips }) {
  return createElement(
    "div",
    { className: "demo-app" },
    createElement("h2", null, "Fiber Demo Counter"),
    createElement(
      "p",
      null,
      "当前数字：",
      createElement("strong", null, String(count)),
    ),
    createElement(
      "div",
      { className: "button-row" },
      createElement(
        "button",
        { onClick: () => update({ count: state.count + 1 }) },
        "加一，触发 UPDATE",
      ),
      createElement(
        "button",
        {
          className: "secondary",
          onClick: () => update({ showTips: !state.showTips }),
        },
        showTips ? "删除列表，触发 DELETION" : "恢复列表，触发 PLACEMENT",
      ),
    ),
    showTips
      ? createElement(
          "ul",
          null,
          createElement("li", null, "虚拟 DOM：先描述 UI"),
          createElement("li", null, "Fiber：把任务拆成小单元"),
          createElement("li", null, "双树：current / workInProgress"),
        )
      : null,
  );
}

function App() {
  return createElement(CounterCard, state);
}

function update(patch = {}) {
  state = { ...state, ...patch };
  pushLog("----------------------------------------");
  pushLog(
    `触发更新：count=${state.count}, showTips=${String(state.showTips)}`,
  );
  render(createElement(App, null), root);
}

update();
