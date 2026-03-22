## MODIFIED Requirements

### Requirement: Agent 构建器
系统 MUST 提供一个构建器函数，使用 LangChain 的 `create_react_agent` 初始化智能体。该构建器 SHALL 确保传入的 LLM 实例已正确配置，并使用新版的 `langchain.agents.create_react_agent` API。

#### Scenario: 成功构建基于 Kimi 的智能体
- **WHEN** 调用 `builder.create_agent(kimi_llm, tools, prompt)`
- **THEN** 返回一个配置了 Kimi 模型且通过新版 `create_react_agent` 构建的智能体实例。
