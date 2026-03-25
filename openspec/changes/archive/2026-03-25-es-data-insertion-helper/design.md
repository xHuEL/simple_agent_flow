# Design: ES Data Insertion Helper

## 概述

本设计文档描述了从文本文件读取槽位数据并插入到Elasticsearch的数据插入助手类的实现方案。

## 架构设计

### 类结构

```
ESDataInsertionHelper
├── __init__(config: dict)          # 初始化ES客户端
├── parse_file(file_path: str)      # 解析文本文件
├── insert_data(index_name: str)    # 插入数据到指定索引
├── validate_data(data: list)       # 数据验证
└── close()                         # 关闭ES连接
```

### 文件解析策略

支持多种文本格式：
1. **CSV格式**: 逗号分隔，字段顺序: slotName,slotReName,slotType
2. **TSV格式**: 制表符分隔，字段顺序: slotName\tslotReName\tslotType  
3. **固定格式**: 每行固定位置，通过配置指定字段位置

### 数据格式

```
# CSV 示例
"用户姓名","user_name","string"
"用户年龄","user_age","number"
"用户地址","user_address","string"

# TSV 示例
用户姓名\tuser_name\tstring
用户年龄\tuser_age\tnumber
用户地址\tuser_address\tstring
```

## 实现细节

### 1. 文件解析器

```python
def parse_file(self, file_path: str) -> List[Dict]:
    """
    解析文本文件，自动检测格式并返回结构化数据
    
    Args:
        file_path: 文本文件路径
        
    Returns:
        List[Dict]: 解析后的数据列表，每个元素包含slotName, slotReName, slotType
    """
```

### 2. 数据验证

```python
def validate_data(self, data: List[Dict]) -> Tuple[bool, List[str]]:
    """
    验证数据完整性
    
    Args:
        data: 待验证的数据列表
        
    Returns:
        Tuple[bool, List[str]]: (是否有效, 错误消息列表)
    """
```

### 3. 数据插入

```python
def insert_data(self, index_name: str, data: List[Dict]) -> Dict:
    """
    批量插入数据到Elasticsearch
    
    Args:
        index_name: 目标索引名称
        data: 要插入的数据列表
        
    Returns:
        Dict: 插入操作的结果统计
    """
```

## 错误处理

- 文件不存在或无法读取
- 文件格式不支持
- 数据格式错误
- ES连接失败
- 索引不存在时自动创建

## 集成点

- 使用现有的 `common.es_client.ESClient`
- 保持与现有索引创建工具的兼容性
- 支持命令行接口和程序化调用