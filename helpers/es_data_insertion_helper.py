#!/usr/bin/env python3
"""
Elasticsearch 数据插入工具 (ES Data Insertion Helper)

从文本文件读取槽位数据并插入到Elasticsearch索引的工具。
支持CSV和TSV格式的文件解析。
"""

import argparse
import csv
import sys
import os
from typing import List, Dict, Tuple, Optional
from common.es_client import ESClient


class ESDataInsertionHelper:
    """Elasticsearch 数据插入助手类"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化ES数据插入助手
        
        Args:
            config: ES客户端配置字典
        """
        self.config = config or {
            "ES_HOST": "localhost",
            "ES_PORT": "9200",
            "request_timeout": 300
        }
        self.client = None
        self.connected = False
    
    def connect(self) -> None:
        """连接到Elasticsearch"""
        try:
            self.client = ESClient(self.config)
            self.client.connect()
            self.connected = True
            print(f"已连接到 Elasticsearch: {self.config['ES_HOST']}:{self.config['ES_PORT']}")
        except Exception as e:
            print(f"连接Elasticsearch失败: {str(e)}")
            raise
    
    def parse_file(self, file_path: str, file_format: str = "auto") -> List[Dict]:
        """
        解析文本文件，返回结构化数据
        
        Args:
            file_path: 文件路径
            file_format: 文件格式 (auto/csv/tsv)
            
        Returns:
            List[Dict]: 解析后的数据列表
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 自动检测文件格式
        if file_format == "auto":
            file_format = self._detect_file_format(file_path)
        
        print(f"解析文件: {file_path} (格式: {file_format})")
        
        if file_format == "csv":
            return self._parse_csv(file_path)
        elif file_format == "tsv":
            return self._parse_tsv(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {file_format}")
    
    def _detect_file_format(self, file_path: str) -> str:
        """自动检测文件格式"""
        if file_path.endswith('.csv'):
            return "csv"
        elif file_path.endswith('.tsv') or file_path.endswith('.txt'):
            # 检查文件内容来确定是TSV还是其他格式
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if '\t' in first_line:
                    return "tsv"
                elif ',' in first_line:
                    return "csv"
        return "tsv"  # 默认尝试TSV格式
    
    def _parse_csv(self, file_path: str) -> List[Dict]:
        """解析CSV文件"""
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader, 1):
                if not row or all(not cell.strip() for cell in row):
                    continue  # 跳过空行
                
                if len(row) < 3:
                    print(f"警告: 第{i}行字段不足，跳过")
                    continue
                
                data.append({
                    "slotName": row[0].strip(),
                    "slotReName": row[1].strip(),
                    "slotType": row[2].strip()
                })
        return data
    
    def _parse_tsv(self, file_path: str) -> List[Dict]:
        """解析TSV文件"""
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue  # 跳过空行
                
                parts = line.split('\t')
                if len(parts) < 3:
                    print(f"警告: 第{i}行字段不足，跳过")
                    continue
                
                data.append({
                    "slotName": parts[0].strip(),
                    "slotReName": parts[1].strip(),
                    "slotType": parts[2].strip()
                })
        return data
    
    def validate_data(self, data: List[Dict]) -> Tuple[bool, List[str]]:
        """
        验证数据完整性
        
        Args:
            data: 待验证的数据列表
            
        Returns:
            Tuple[bool, List[str]]: (是否有效, 错误消息列表)
        """
        errors = []
        valid = True
        seen_slot_renames = set()
        
        valid_slot_types = {"string", "number", "boolean", "date"}
        
        for i, item in enumerate(data, 1):
            # 检查必填字段
            if not item.get("slotName"):
                errors.append(f"第{i}行: slotName不能为空")
                valid = False
            
            if not item.get("slotReName"):
                errors.append(f"第{i}行: slotReName不能为空")
                valid = False
            elif item["slotReName"] in seen_slot_renames:
                errors.append(f"第{i}行: slotReName '{item['slotReName']}' 重复")
                valid = False
            else:
                seen_slot_renames.add(item["slotReName"])
            
            if not item.get("slotType"):
                errors.append(f"第{i}行: slotType不能为空")
                valid = False
            elif item["slotType"] not in valid_slot_types:
                errors.append(f"第{i}行: 无效的slotType '{item['slotType']}'，必须是 {valid_slot_types}")
                valid = False
        
        return valid, errors
    
    def insert_data(self, index_name: str, data: List[Dict], batch_size: int = 100) -> Dict:
        """
        批量插入数据到Elasticsearch
        
        Args:
            index_name: 目标索引名称
            data: 要插入的数据列表
            batch_size: 批量插入大小
            
        Returns:
            Dict: 插入操作的结果统计
        """
        if not self.connected:
            self.connect()
        
        print(f"开始向索引 {index_name} 插入 {len(data)} 条数据...")
        
        # 确保索引存在
        if not self.client.index_exists(index_name):
            print(f"索引 {index_name} 不存在，正在创建...")
            from es_create_index_helper import create_slot_index
            create_slot_index(self.client, index_name)
        
        success_count = 0
        error_count = 0
        
        # 批量插入
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            bulk_actions = []
            
            for item in batch:
                bulk_actions.append({"index": {"_index": index_name}})
                bulk_actions.append(item)
            
            try:
                response = self.client.bulk(bulk_actions)
                if response.get("errors"):
                    for item in response.get("items", []):
                        if "error" in item.get("index", {}):
                            error_count += 1
                        else:
                            success_count += 1
                else:
                    success_count += len(batch)
                
                print(f"已处理: {min(i + batch_size, len(data))}/{len(data)} 条数据")
                
            except Exception as e:
                error_count += len(batch)
                print(f"批量插入失败: {str(e)}")
        
        stats = {
            "total": len(data),
            "success": success_count,
            "errors": error_count,
            "success_rate": success_count / len(data) if data else 0
        }
        
        print(f"插入完成! 成功: {success_count}, 失败: {error_count}, 成功率: {stats['success_rate']:.1%}")
        return stats
    
    def close(self) -> None:
        """关闭ES连接"""
        if self.client:
            self.client.close()
            self.connected = False
            print("ES连接已关闭")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Elasticsearch 数据插入工具")
    parser.add_argument("--file", "-f", required=True, help="输入文件路径 (CSV/TSV格式)")
    parser.add_argument("--index", "-i", default="slot_index", help="目标索引名称 (默认: slot_index)")
    parser.add_argument("--format", "-t", default="auto", choices=["auto", "csv", "tsv"], 
                       help="文件格式 (默认: auto)")
    parser.add_argument("--host", default="localhost", help="Elasticsearch 主机 (默认: localhost)")
    parser.add_argument("--port", type=int, default=9200, help="Elasticsearch 端口 (默认: 9200)")
    parser.add_argument("--batch-size", type=int, default=100, help="批量插入大小 (默认: 100)")
    
    args = parser.parse_args()
    
    # 配置 ES 客户端
    config = {
        "ES_HOST": args.host,
        "ES_PORT": str(args.port),
        "request_timeout": 300
    }
    
    helper = None
    try:
        helper = ESDataInsertionHelper(config)
        
        # 解析文件
        data = helper.parse_file(args.file, args.format)
        print(f"成功解析 {len(data)} 条数据")
        
        # 验证数据
        is_valid, errors = helper.validate_data(data)
        if not is_valid:
            print("数据验证失败:")
            for error in errors:
                print(f"  {error}")
            print("请修复数据文件后重试")
            sys.exit(1)
        
        # 插入数据
        helper.connect()
        result = helper.insert_data(args.index, data, args.batch_size)
        
        if result["errors"] > 0:
            sys.exit(1)
            
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)
        
    finally:
        if helper:
            helper.close()


if __name__ == "__main__":
    main()