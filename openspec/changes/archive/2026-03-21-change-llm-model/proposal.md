## Why

当前系统使用的是 OpenAI 的模型，为了支持国产模型并降低成本，计划将 LLM 切换为 Kimi (Moonshot AI) 模型。此外，为了增强安全性，API 密钥将不再从 `.env` 中读取，而是从命令行参数指定的配置文件 `config/.config` 中读取。

## What Changes

- **LLM 切换**: 将 `ChatOpenAI` 替换为适配 Kimi 的 `ChatMoonshot` 或使用兼容 OpenAI 接口的配置方式接入 Kimi 模型。
- **配置读取方式修改**: 实现从 `config/.config` 文件中解析 API 密钥的逻辑。
- **依赖更新**: 如果使用 Kimi 原生 SDK，需要更新 `requirements.txt`。
- **环境变量移除**: 移除对 `OPENAI_API_KEY` 的依赖。

## Capabilities

### New Capabilities
- `kimi-integration`: 集成 Kimi (Moonshot AI) 模型作为系统的核心推理引擎。
- `external-config-loader`: 实现从特定路径 (`config/.config`) 加载敏感配置信息的能力。

### Modified Capabilities
- `agent-core`: 修改智能体构建逻辑，以支持新的模型接入方式。

## Impact

- **Breaking Change**: 移除对 OpenAI 的直接支持。
- **配置变更**: 用户需要创建 `config/.config` 文件并填入 Kimi API Key，而不是使用 `.env`。
- **依赖**: 引入 `langchain-moonshot` 或更新 `langchain-openai` 的 base_url。
- **Token 消耗**: Kimi 的 Token 计费和消耗模式与 OpenAI 略有不同，需要重新关注长上下文的处理。
