## 1. 核心代码迁移

- [x] 1.1 在 `agent/builder.py` 中将 `from langchain.agents import create_agent` 修改为 `from langchain.agents import create_react_agent`
- [x] 1.2 更新 `create_agent` 函数实现，调用 `create_react_agent` 并确保参数传递正确
- [x] 1.3 确认 `prompt/react_prompt.py` 中的模板与 `create_react_agent` 的占位符要求（`{tools}`, `{tool_names}`, `{input}`, `{agent_scratchpad}`）一致

## 2. 测试更新与验证

- [x] 2.1 更新 `tests/test_agent.py`，将 `patch('langchain.agents.create_agent')` 替换为 `patch('langchain.agents.create_react_agent')`（如果存在相关 Mock）
- [x] 2.2 运行 `python3 -m pytest tests/test_agent.py` 验证智能体构建逻辑
- [x] 2.3 运行 `python3 main.py` 进行集成测试，确保 ReAct 循环正常工作
