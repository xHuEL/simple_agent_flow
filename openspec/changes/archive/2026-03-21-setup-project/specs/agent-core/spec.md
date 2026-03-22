## ADDED Requirements

### Requirement: Agent 构建器
系统 MUST 提供一个构建器函数，使用 LangChain 的 `create_react_agent` 初始化智能体。

#### Scenario: 成功构建智能体
- **WHEN** 调用 `builder.create_agent(llm, tools, prompt)`
- **THEN** 返回一个配置正确的智能体实例。

### Requirement: Agent 执行器封装
系统 MUST 封装 `AgentExecutor` 以支持流式输出和错误处理（如解析错误）。

#### Scenario: 成功执行智能体
- **WHEN** 调用 `executor.run(agent, input)`
- **THEN** 返回智能体的最终答案或处理后的流式输出。
