## Why

当前 `agent/builder.py` 中使用的 `create_agent` 是 LangChain 的旧版 API（已被弃用或不推荐）。为了保持代码的现代性和更好的社区支持，计划将其切换为 `langchain.agents.create_react_agent`。这将有助于解决未来可能的兼容性问题，并提升 ReAct 智能体的稳定性。

## What Changes

- **API 切换**: 将 `langchain.agents.create_agent` 替换为 `langchain.agents.create_react_agent`。
- **构建逻辑调整**: 修改 `agent/builder.py` 以适应新版 API 的参数要求。
- **ReAct 格式确认**: 确保提示词模板与 `create_react_agent` 所需的 ReAct 格式完全匹配。
- **Mock 测试更新**: 更新单元测试中对智能体构建的 Mock 逻辑，以兼容新版 API。

## Capabilities

### New Capabilities
- 无

### Modified Capabilities
- `agent-core`: 修改智能体构建器逻辑，从旧版 `create_agent` 迁移到新版 `create_react_agent`。

## Impact

- **Affected Code**: `agent/builder.py`, `tests/test_agent.py`。
- **Dependencies**: 确保 `langchain` 版本支持 `create_react_agent`（通常是 0.1.0+）。
- **Token 消耗**: 无显著变化，但新版 API 可能会稍微改变推理链的结构。
