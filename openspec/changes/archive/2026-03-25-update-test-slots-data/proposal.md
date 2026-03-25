## Why

需要更新测试数据以更好地反映实际应用场景。当前的测试数据使用通用字段名称，缺乏领域特异性。通过使用阅读领域的真实数据（作者名和书名），可以更有效地测试数据插入工具在真实场景中的表现，同时为后续的阅读相关功能开发提供更好的测试基础。

## What Changes

- 更新现有的测试文件 `test_slots.csv` 和 `test_slots.tsv`
- 将通用测试数据替换为阅读领域的专业数据
- 添加30个真实的作者和书名组合
- 保持原有的数据格式和结构不变
- 确保新的测试数据覆盖各种边界情况

## Capabilities

### New Capabilities
- test-data-reading-domain: 阅读领域测试数据生成能力

### Modified Capabilities
- es-data-insertion: 测试数据内容更新，不影响功能接口

## Impact

- 影响测试文件: `test_slots.csv`, `test_slots.tsv`
- 需要更新相关的测试用例以匹配新的测试数据
- 不影响核心的数据插入功能，只是测试数据内容的变化
- 为后续阅读相关功能的开发提供更真实的测试环境