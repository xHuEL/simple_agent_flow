## Why

需要为项目提供Elasticsearch索引创建测试能力，验证本地ES服务正常运行并能够正确创建特定结构的索引。当前项目缺乏对ES操作的自动化测试，无法确保搜索服务的可靠性。

## What Changes

- 创建测试脚本，用于向本地Elasticsearch新建特定结构的索引
- 索引结构包含：text类型的slotName字段、keyword类型的slotReName字段、槽位slotType字段
- 提供索引创建验证和基本数据操作测试
- 集成到现有测试框架中

## Capabilities

### New Capabilities
- es-index-testing: 提供Elasticsearch索引创建和验证的测试能力

### Modified Capabilities
- 无现有功能修改

## Impact

- 新增测试脚本文件
- 依赖Elasticsearch Python客户端
- 需要本地ES服务运行
- 集成到现有测试框架中