## Why

初始化项目的基础结构和核心组件。目前项目需要一个清晰的分层架构（tools, prompt, agent, tests）来支持基于 LangChain 的 ReAct 智能体系统的开发。这为后续的功能扩展、工具集成和自动化测试奠定基础。

## What Changes

- **基础结构搭建**: 创建 `tools/`, `prompt/`, `agent/`, `tests/` 等核心目录。
- **环境配置**: 提供 `.env.example` 和 `requirements.txt` 以支持项目依赖和环境变量管理。
- **核心组件实现**:
    - 在 `tools/` 中实现基础的搜索和百科工具。
    - 在 `prompt/` 中定义 ReAct 提示词模板。
    - 在 `agent/` 中封装 Agent 构建和执行逻辑。
- **入口程序**: 实现 `main.py` 以支持命令行交互。
- **测试框架**: 配置 `pytest` 并编写基础的单元测试。

## Capabilities

### New Capabilities
- `project-structure`: 初始化项目的分层目录结构和基础配置文件（README, .env, requirements.txt）。
- `react-prompt`: 定义支持中文的 ReAct 提示词模板，确保智能体遵循 Thought/Action/Observation 循环。
- `agent-core`: 封装 LangChain 的 `create_react_agent` 和 `AgentExecutor`，支持流式输出和错误处理。
- `base-tools`: 提供 Web 搜索和 Wikipedia 检索工具，作为智能体的基础外部能力。
- `test-suite`: 建立完整的测试体系，涵盖工具、提示词和智能体逻辑。

### Modified Capabilities
<!-- Existing capabilities whose REQUIREMENTS are changing (not just implementation).
     Only list here if spec-level behavior changes. Each needs a delta spec file.
     Use existing spec names from openspec/specs/. Leave empty if no requirement changes. -->

## Impact

- **代码结构**: 确立了项目的模块化分层模式。
- **依赖**: 引入了 LangChain, OpenAI, pytest 等核心依赖。
- **推理链**: 通过标准的 ReAct 提示词确立了智能体的推理模式。
- **Token 消耗**: 初始化阶段主要涉及提示词模板的加载，单次推理的 Prompt Token 预计在 500-1000 左右，具体取决于工具描述和用户输入的复杂度。
