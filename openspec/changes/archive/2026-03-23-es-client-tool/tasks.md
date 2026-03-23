## 1. 准备工作

- [x] 1.1 在 `requirements.txt` 中添加 `elasticsearch` 依赖
- [x] 1.2 在 `config/.config` 中增加 `ES_HOST`, `ES_PORT`, `ES_USER`, `ES_PASSWORD` 占位符

## 2. Common SDK 开发

- [x] 2.1 创建 `common/` 目录（如果不存在）
- [x] 2.2 在 `common/` 下创建 `es_client.py`，实现 `ESClient` 类并包含连接逻辑和搜索方法
- [x] 2.3 在 `main.py` 中更新配置加载逻辑，支持读取 Elasticsearch 相关的配置项

## 3. 工具集成

- [x] 3.1 在 `tools/` 下创建 `es_search_tool.py`，导入 `common.es_client` 并实现基于 `@tool` 的智能体工具
- [x] 3.2 在 `main.py` 中导入并注册 `es_search_tool` 到智能体工具列表中

## 4. 验证与测试

- [x] 4.1 编写 `tests/test_es_client.py`，验证 `common.es_client` 的连接和搜索逻辑
- [x] 4.2 运行集成测试，确保智能体能够识别并正确调用 `es_search_tool`
