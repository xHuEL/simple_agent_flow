import json
import os
from typing import List, Optional
from langchain_core.tools import tool


def read_json_categories(file_path: str) -> List[str]:
    """从 JSON 文件中读取分类信息。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            categories = json.load(f)
        
        if not isinstance(categories, list):
            raise ValueError("JSON 文件应该包含一个分类列表")
        
        # 确保所有分类都是字符串
        return [str(category) for category in categories if category]
    
    except json.JSONDecodeError:
        raise ValueError("JSON 文件格式错误")
    except Exception as e:
        raise ValueError(f"读取 JSON 文件失败: {e}")


def format_categories(categories: List[str]) -> str:
    """格式化分类信息为字符串。"""
    if not categories:
        return "未找到分类信息。"
    
    formatted = []
    for i, category in enumerate(categories, 1):
        formatted.append(f"{i}. {category}")
    
    return "\n".join(formatted)


@tool
def reading_category_tool(file_path: str) -> str:
    """
    从文件中读取阅读领域的所有分类信息并以列表字符串格式返回。
    
    该工具支持 JSON 文件格式，能够自动检测文件类型并解析分类信息。
    适合用于获取阅读推荐系统的分类体系或内容管理系统的分类结构。

    Args:
        file_path: 分类文件路径，支持 JSON 格式

    Returns:
        一个字符串，包含格式化后的分类列表，每个分类前有序号。
        如果文件不存在或格式错误，返回友好的错误信息。
    """
    
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return f"错误: 文件 '{file_path}' 不存在。"
        
        # 检查文件扩展名
        if not file_path.lower().endswith('.json'):
            return f"错误: 不支持的文件格式 '{file_path}'。目前仅支持 JSON 格式。"
        
        # 读取分类信息
        categories = read_json_categories(file_path)
        
        # 格式化结果
        return format_categories(categories)
        
    except ValueError as e:
        return f"错误: {e}"
    except Exception as e:
        return f"读取分类信息时发生未知错误: {e}"