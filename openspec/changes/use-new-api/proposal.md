## Why

LangChain 0.1.0+ (v1) 引入了更稳定、标准化的 API 用于构建智能体和处理工具调用。当前系统部分实现仍在使用旧版模式，为了确保系统的长期可维护性、更好的错误处理以及与 LangChain 生态系统的最佳集成，有必要将核心智能体逻辑重构到新版 API。

## What Changes

- **依赖更新**: 在 `requirements.txt` 中将 `langchain` 及其相关组件版本锁定在 0.1.0 或更高版本。
- **构建器重构**: 修改 `agent/builder.py`，使用 `langchain.agents.create_react_agent` 替代旧的构建方式。
- **执行器优化**: 调整 `agent/executor.py` 中的 `AgentExecutor` 配置，以利用新版提供的改进（如更好的解析错误处理）。
- **提示词适配**: 确保 `prompt/react_prompt.py` 中的占位符（如 `tools`, `tool_names`, `agent_scratchpad`）与新版 `create_react_agent` 完全兼容。
- **测试更新**: 更新 `tests/test_agent.py` 中的 Mock 逻辑和测试用例，以匹配新的 API 调用结构。

## Capabilities

### New Capabilities
- 无

### Modified Capabilities
- `agent-core`: 更新核心智能体构建与执行逻辑，以适配 LangChain v1 API。

## Impact

- **Affected Code**: `agent/builder.py`, `agent/executor.py`, `prompt/react_prompt.py`, `requirements.txt`, `tests/test_agent.py`。
- **Dependencies**: 强制要求 `langchain>=0.1.0`。
- **BREAKING**: 修改了智能体内部初始化逻辑，虽然对外接口尽量保持一致，但底层实现已完全迁移。
