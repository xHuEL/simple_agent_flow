## MODIFIED Requirements

### Requirement: Agent 构建器
系统 MUST 提供一个构建器函数，使用 LangChain v1 标准的 `create_react_agent` 初始化智能体。该构建器 SHALL 确保传入的 LLM 实例已正确配置，且提示词模板包含所有必需的占位符。

#### Scenario: 成功构建标准 ReAct 智能体
- **WHEN** 调用 `builder.create_agent(llm, tools, prompt)`
- **THEN** 返回一个符合 LangChain v1 标准的智能体 Runnable 实例。

### Requirement: Agent 执行器封装
系统 MUST 封装 `AgentExecutor` 以支持最新的 API 调用方式（如 `.invoke()`），并开启鲁棒的错误处理。

#### Scenario: 成功执行并处理解析错误
- **WHEN** 调用 `executor.run_agent(executor, input_text)` 且 LLM 返回非标准格式
- **THEN** 执行器 SHALL 能够捕获解析错误并尝试自我修复，最终返回有效输出。
