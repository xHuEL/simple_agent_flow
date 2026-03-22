## ADDED Requirements

### Requirement: Web 搜索工具
系统 MUST 提供一个 Web 搜索工具，支持根据关键字检索外部网页内容。

#### Scenario: 成功搜索
- **WHEN** 调用 `search_tool.run("Python ReAct agent")`
- **THEN** 返回相关的网页搜索结果片段。

### Requirement: Wikipedia 检索工具
系统 MUST 提供一个 Wikipedia 检索工具，支持检索维基百科上的知识条目。

#### Scenario: 成功检索维基百科
- **WHEN** 调用 `wikipedia_tool.run("LangChain")`
- **THEN** 返回该条目的摘要。

### Requirement: 工具签名规范
所有工具 MUST 使用 `@tool` 装饰器，包含明确的类型注解和文档字符串（docstring）。

#### Scenario: 验证工具签名
- **WHEN** 检查工具定义
- **THEN** 每个工具 MUST 有参数类型提示和描述其用途的 docstring。
