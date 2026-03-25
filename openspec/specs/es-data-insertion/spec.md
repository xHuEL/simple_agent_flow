# Specification: ES Data Insertion

## 功能规格

### 1. 文件解析功能

#### 输入格式支持
- **CSV格式**: 逗号分隔值文件
  - 字段顺序: slotName, slotReName, slotType
  - 支持引号包裹的字段值
  - 示例: `"用户姓名","user_name","string"`

- **TSV格式**: 制表符分隔值文件  
  - 字段顺序: slotName\tslotReName\tslotType
  - 示例: `用户姓名\tuser_name\tstring`

- **自动检测**: 根据文件扩展名和内容自动识别格式

#### 文件要求
- 文件编码: UTF-8
- 文件扩展名: .csv, .tsv, .txt
- 支持无表头和有表头文件

### 2. 数据验证规则

#### 字段验证
- **slotName**: 必填字段，字符串类型，长度1-255字符
- **slotReName**: 必填字段，字符串类型，符合标识符命名规范（字母、数字、下划线）
- **slotType**: 必填字段，枚举值: "string", "number", "boolean", "date"

#### 业务规则
- 不允许重复的 slotReName
- slotName 可以重复但会生成警告
- 空行自动跳过
- 格式错误的行记录错误并继续处理

### 3. Elasticsearch 集成

#### 索引要求
- 目标索引: slot_index
- 索引映射必须包含:
  - slotName: text类型
  - slotReName: keyword类型  
  - slotType: keyword类型

#### 插入策略
- 批量插入，每批100条记录
- 支持幂等操作（相同slotReName会覆盖）
- 插入前检查索引是否存在，不存在则自动创建

### 4. 错误处理

#### 错误级别
- **警告**: 数据格式问题但可继续处理
- **错误**: 严重问题导致处理中断

#### 错误报告
- 控制台输出详细错误信息
- 返回处理统计信息
- 支持错误日志文件输出

## 接口规范

### 命令行接口

```bash
# 基本用法
python es_data_insertion_helper.py --file data.txt --index slot_index

# 指定ES连接
python es_data_insertion_helper.py --file data.csv --index slot_index --host localhost --port 9200

# 指定文件格式
python es_data_insertion_helper.py --file data.txt --format csv --index slot_index
```

#### 参数说明
- `--file, -f`: 输入文件路径（必需）
- `--index, -i`: 目标索引名称（默认: slot_index）
- `--format, -t`: 文件格式（auto/csv/tsv，默认: auto）
- `--host`: Elasticsearch主机（默认: localhost）
- `--port`: Elasticsearch端口（默认: 9200）
- `--batch-size`: 批量插入大小（默认: 100）

### 程序化接口

```python
from es_data_insertion_helper import ESDataInsertionHelper

# 初始化
helper = ESDataInsertionHelper({
    "ES_HOST": "localhost",
    "ES_PORT": "9200"
})

# 解析文件
data = helper.parse_file("data.txt")

# 插入数据
result = helper.insert_data("slot_index", data)

# 关闭连接
helper.close()
```

## 性能要求

- 支持处理10,000+条记录的文件
- 内存使用优化，支持流式处理大文件
- 批量插入优化，减少ES请求次数
- 处理速度: ≥ 1000条/秒（在标准硬件上）

## 兼容性

- Python 3.7+
- Elasticsearch 7.x+
- 支持Windows/Linux/macOS