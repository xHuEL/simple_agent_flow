## Why

当前系统缺乏对外部数据库（特别是 Elasticsearch）的直接访问能力。为了支持更复杂的知识检索和数据查询任务，需要开发一个专门的 Elasticsearch 调用 SDK。将该 SDK 放置在 `common/` 目录下，可以确保其作为通用组件在多个工具或模块中被重用。这将使智能体能够执行精确的全文搜索、结构化数据查询以及日志分析等任务，从而扩展其知识边界和解决问题的能力。

## What Changes

- **新增依赖**: 在 `requirements.txt` 中添加 `elasticsearch` 客户端库。
- **SDK 实现**: 在 `common/` 目录下创建一个新的 `es_client.py`，实现一个通用的 Elasticsearch 客户端封装。
- **工具集成**: 基于该 SDK，在 `tools/` 目录下创建一个 `es_search_tool.py`，供智能体调用。
- **配置支持**: 在 `config/.config` 中增加 Elasticsearch 相关的配置项（如 `ES_HOST`, `ES_PORT`, `ES_USER`, `ES_PASSWORD`）。

## Capabilities

### New Capabilities
- `es-client-tool`: 提供与 Elasticsearch 集群交互的基础能力，包括连接管理、索引查询和文档检索。该能力以通用 SDK 形式实现在 `common/` 目录中。

### Modified Capabilities
- 无

## Impact

- **Affected Code**: `common/es_client.py` (new), `tools/es_search_tool.py` (new), `requirements.txt`, `config/.config`。
- **Dependencies**: 引入 `elasticsearch` 官方 Python SDK。
- **Configuration**: 需要用户提供有效的 Elasticsearch 集群连接信息。
