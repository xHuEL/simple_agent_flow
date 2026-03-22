## ADDED Requirements

### Requirement: ReAct 提示词模板
系统 MUST 定义一个支持中文的 ReAct 提示词模板，确保智能体遵循 Thought/Action/Observation/Final Answer 的推理链。

#### Scenario: 验证提示词格式
- **WHEN** 调用提示词模板
- **THEN** 输出 MUST 包含 "Thought:", "Action:", "Action Input:", "Observation:", "Final Answer:" 及其对应的中文引导。

### Requirement: 工具描述注入
提示词模板 MUST 支持动态注入工具列表及其描述。

#### Scenario: 注入工具描述
- **WHEN** 给定工具列表（如 search, wikipedia）
- **THEN** 生成的提示词中 MUST 包含这些工具的名称和用法说明。
