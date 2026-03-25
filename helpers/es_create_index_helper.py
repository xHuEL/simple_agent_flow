#!/usr/bin/env python3
"""
Elasticsearch 索引创建工具 (ES Create Index Helper)

专门用于创建Elasticsearch索引的工具，支持创建特定结构的索引。
主要用于创建slot_index索引结构。
"""

import argparse
import sys
from common.es_client import ESClient


def create_slot_index(client: ESClient, index_name: str):
    """创建槽位索引结构"""
    # 定义索引映射结构
    mapping = {
        "properties": {
            "slotName": {
                "type": "text",
                "analyzer": "standard"
            },
            "slotReName": {
                "type": "keyword"
            },
            "slotType": {
                "type": "keyword"
            }
        }
    }
    
    print(f"正在创建索引: {index_name}")
    response = client.create_index(index_name, mapping)
    print(f"创建成功: {response}")
    return response


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Elasticsearch 索引创建工具")
    parser.add_argument("--index", "-i", default="slots_index", 
                       help="索引名称 (默认: slots_index)")
    parser.add_argument("--host", default="localhost",
                       help="Elasticsearch 主机 (默认: localhost)")
    parser.add_argument("--port", type=int, default=9200,
                       help="Elasticsearch 端口 (默认: 9200)")
    
    args = parser.parse_args()
    
    # 配置 ES 客户端
    config = {
        "ES_HOST": args.host,
        "ES_PORT": str(args.port),
        "request_timeout": 300
    }
    
    try:
        client = ESClient(config)
        client.connect()
        print(f"已连接到 Elasticsearch: {args.host}:{args.port}")
        
        # 创建索引
        create_slot_index(client, args.index)
        print("索引创建完成！")
        
    except Exception as e:
        print(f"错误: {str(e)}")
        print("请检查 Elasticsearch 服务是否运行")
        sys.exit(1)


if __name__ == "__main__":
    main()