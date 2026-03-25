## Why

需要为项目提供从文本文件读取数据并插入到Elasticsearch的能力，方便批量导入槽位数据。当前项目缺乏从文件批量导入数据的功能，手动插入数据效率低下。

## What Changes

- 重命名 `es_data_helper.py` 为 `es_create_index_helper.py`，专注于索引创建
- 创建新的数据插入助手类，从文本文件读取槽位数据
- 支持多种文本格式解析（CSV、TSV、固定格式等）
- 提供数据验证和错误处理机制
- 插入数据到指定的slot_index索引

## Capabilities

### New Capabilities
- es-data-insertion: 从文本文件读取数据并插入到Elasticsearch的能力
- file-data-parser: 多种文本格式解析能力

### Modified Capabilities
- es-index-creation: 重命名和重构现有的索引创建功能

## Impact

- 重命名现有文件：es_data_helper.py → es_create_index_helper.py
- 新增数据插入助手类
- 新增文本文件解析功能
- 需要处理文件读取和格式解析
- 集成到现有ES客户端架构中