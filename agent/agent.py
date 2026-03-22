from typing import Dict, Any

from langchain.agents import create_react_agent, AgentExecutor, AgentOutputParser
import json

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult
from langchain_core.exceptions import OutputParserException


class ToolTraceHandler(BaseCallbackHandler):
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs) -> None:
        print(f"[工具调用开始] {serialized.get('name')} 输入: {input_str}")

    def on_tool_end(self, output: str, **kwargs) -> None:
        print(f"[工具调用结束] 输出: {output[:200]}")  # 截断输出


class AgentCallbackHandler(BaseCallbackHandler):
    def on_agent_action(self, action: AgentAction, **kwargs):
        print(f"🎯 Agent 选择动作: {action.tool}，输入: {action.tool_input}")

    def on_agent_finish(self, finish: AgentFinish, **kwargs):
        print(f"🏁 Agent 完成: {finish.return_values}")

def run_agent(agent, tools, max_iterations, query):
    # 创建 executor 时传入回调
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        max_iterations=5,
        early_stopping_method="force",
        verbose=True,  # 关闭默认打印，由回调控制
        callbacks=[ToolTraceHandler(), AgentCallbackHandler()]
    )

    # 运行（同步）
    agent_executor.invoke({"input": query})


def create_agent(
    model: str = None,
    tools: list = None,
    system_prompt = None,
):
    # 使用 create_react_agent 构建基于 LangChain 的 ReAct 循环
    agent = create_react_agent(
        llm=model,
        tools=tools,
        prompt=system_prompt,
    )
 
    return agent