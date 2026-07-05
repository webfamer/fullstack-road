"""演示 LangGraph 中 reducer 与 checkpoint 的分工。

运行：
    python/.venv/bin/pip install -U langgraph
    python/.venv/bin/python python/examples/langgraph_state_checkpoint_demo.py

本示例不调用任何大模型，也不需要 API Key。
"""

from typing import Annotated

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph, add_messages
from typing_extensions import TypedDict


class ChatState(TypedDict, total=False):
    # 有 reducer：新消息会与旧消息合并，而不是直接覆盖。
    messages: Annotated[list[BaseMessage], add_messages]
    # 无 reducer：节点返回新值时，默认覆盖旧值。
    question: str
    answer: str


def message_text(message: BaseMessage) -> str:
    """把消息内容转成适合终端展示的字符串。"""
    return str(message.content)


def print_state(title: str, state: ChatState) -> None:
    print(f"\n{title}")
    print(f"  question = {state.get('question')!r}")
    print(f"  answer   = {state.get('answer')!r}")
    print("  messages =")
    for index, message in enumerate(state.get("messages", []), start=1):
        print(
            f"    {index}. {message.type:<5} "
            f"id={message.id!r} content={message_text(message)!r}"
        )


def answer_node(state: ChatState) -> ChatState:
    """返回部分 state update；LangGraph 会在节点结束后执行 reducer。"""
    print_state("[节点收到的完整 State]", state)

    answer = f"你问的是：{state['question']}"
    update: ChatState = {
        "messages": [AIMessage(content=answer)],
        "answer": answer,
    }

    print("\n[节点只返回部分 State update]")
    print(f"  answer   = {update['answer']!r}")
    print(f"  messages = {[message_text(m) for m in update['messages']]}")
    return update


def build_graph():
    builder = StateGraph(ChatState)
    builder.add_node("answer", answer_node)
    builder.add_edge(START, "answer")
    builder.add_edge("answer", END)

    # InMemorySaver 适合演示和测试；进程退出后数据会消失。
    return builder.compile(checkpointer=InMemorySaver())


def main() -> None:
    graph = build_graph()
    config = {"configurable": {"thread_id": "demo-thread-001"}}

    turns = ["什么是 reducer？", "那 checkpoint 呢？"]
    for turn_number, question in enumerate(turns, start=1):
        print("\n" + "=" * 72)
        print(f"第 {turn_number} 轮调用，同一个 thread_id，用户问题：{question}")

        result = graph.invoke(
            {
                "messages": [HumanMessage(content=question)],
                "question": question,
            },
            config,
        )
        print_state("[invoke 返回的合并后 State]", result)

        snapshot = graph.get_state(config)
        print_state("[checkpointer 中最新 StateSnapshot.values]", snapshot.values)
        print(f"  checkpoint_id = {snapshot.config['configurable']['checkpoint_id']}")

    history = list(graph.get_state_history(config))
    print("\n" + "=" * 72)
    print("Checkpoint 历史（官方 API 默认从新到旧）：")
    for snapshot in history:
        values = snapshot.values
        print(
            f"  step={snapshot.metadata.get('step'):>2} "
            f"source={snapshot.metadata.get('source'):<5} "
            f"messages={len(values.get('messages', []))} "
            f"question={values.get('question')!r} "
            f"answer={values.get('answer')!r}"
        )

    print("\n结论：messages 累积了 4 条；question 和 answer 被第二轮的新值覆盖。")


if __name__ == "__main__":
    main()
