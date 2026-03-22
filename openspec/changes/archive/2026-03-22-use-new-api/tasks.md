## 1. 依赖与基础准备

- [x] 1.1 更新 `requirements.txt`，锁定 `langchain>=0.1.0` 和 `langchain-openai>=0.1.0`
- [x] 1.2 检查并确认 `prompt/react_prompt.py` 中的模板包含 `{input}`, `{tools}`, `{tool_names}`, `{agent_scratchpad}` 占位符

## 2. 核心逻辑重构

- [x] 2.1 修改 `agent/builder.py`：移除旧版 `create_agent` 调用，改用 `langchain.agents.create_react_agent`
- [x] 2.2 修改 `agent/executor.py`：确保 `AgentExecutor` 配置了 `handle_parsing_errors=True`
- [x] 2.3 适配执行器调用方式：在 `agent/executor.py` 中将 `executor.run()` 或旧调用改为 `executor.invoke()`

## 3. 验证与测试

- [x] 3.1 更新 `tests/test_agent.py`：调整 Mock 逻辑以模拟 `create_react_agent` 的行为
- [x] 3.2 运行本地测试：执行 `python3 -m pytest tests/` 确保核心流程无损
- [x] 3.3 集成验证：运行 `python3 main.py` 确认 ReAct 循环在真实（或 Mock）LLM 下工作正常
