## ADDED Requirements

### Requirement: Kimi 模型集成
系统 MUST 使用 Kimi (Moonshot AI) 模型作为主要的推理引擎。

#### Scenario: 成功初始化 Kimi 模型
- **WHEN** 提供正确的 Kimi API Key
- **THEN** 系统能够成功创建 Kimi 的 ChatModel 实例并与之通信。

### Requirement: 外部配置文件加载
系统 MUST 支持从命令行参数指定的路径或默认路径 `config/.config` 中加载配置信息。

#### Scenario: 成功加载配置文件
- **WHEN** 配置文件 `config/.config` 包含 `KIMI_API_KEY=xxx`
- **THEN** 系统能够正确解析并使用该 API 密钥，而不再依赖环境变量。
