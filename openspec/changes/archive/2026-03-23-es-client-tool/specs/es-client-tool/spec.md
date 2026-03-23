## ADDED Requirements

### Requirement: Elasticsearch 客户端封装 (Common SDK)
系统 SHALL 提供一个 `ESClient` 类，封装官方 `elasticsearch` 客户端。该类 MUST 放置在 `common/es_client.py` 中，支持从配置中加载连接信息并管理连接生命周期。

#### Scenario: 成功连接并执行搜索
- **WHEN** 提供有效的 `ES_HOST`, `ES_PORT` 且调用 `client.search(index, query)`
- **THEN** 系统 SHALL 返回包含匹配文档的列表。

### Requirement: Elasticsearch 搜索工具
系统 SHALL 提供一个 `@tool` 装饰的 `es_search_tool`，放置在 `tools/es_search_tool.py` 中。该工具 MUST 导入并使用 `common.es_client`。

#### Scenario: 智能体通过工具获取 ES 数据
- **WHEN** 智能体调用 `es_search_tool(query="error log")`
- **THEN** 工具 SHALL 返回格式化后的字符串结果，包含相关文档的内容。

### Requirement: 配置项支持
系统 SHALL 支持在 `config/.config` 中定义 `ES_HOST`, `ES_PORT`, `ES_USER`, `ES_PASSWORD` 等配置项。

#### Scenario: 缺少配置时的错误处理
- **WHEN** `config/.config` 中缺少 `ES_HOST` 且尝试初始化 `ESClient`
- **THEN** 系统 SHALL 抛出明确的配置错误异常。
