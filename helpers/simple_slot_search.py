# -*- coding: utf-8 -*-
"""
简化版槽位搜索工具 - 使用 match_phrase 查询从槽位中进行搜索
"""

from common.es_client import ESClient


def search_slots_with_match_phrase(query, index="slots_index", es_client=None):
    """
    使用 match_phrase 查询从槽位索引中搜索，返回原始结果数据。
    
    Args:
        query: 要搜索的短语
        index: Elasticsearch 索引名称
        es_client: 可选的 ESClient 实例
        
    Returns:
        包含匹配槽位信息的字典列表，每个字典包含 slotName 和 slotType
    """
    
    client = es_client or ESClient()
    if not es_client:
        client.connect()
    
    # 构建 match_phrase 查询
    search_query = {
        "match_phrase": {
            "slotName": query
        }
    }
    
    # 执行搜索
    results = client.search(index=index, query=search_query, size=20)
    
    # 提取需要的字段
    formatted_results = []
    for slot in results:
        formatted_results.append({
            "slotName": slot.get('slotName'),
            "slotType": slot.get('slotType'),
            "slotReName": slot.get('slotReName', '')
        })
    
    return formatted_results


def format_slot_search_results(results, query):
    """格式化槽位搜索结果"""
    if not results:
        return "未找到与 '{}' 相关的槽位信息。".format(query)
    
    formatted_results = []
    for i, slot in enumerate(results, 1):
        slot_name = slot.get('slotName', '未知槽位名')
        slot_type = slot.get('slotType', '未知类型')
        slot_rename = slot.get('slotReName', '')
        
        result_line = "{}. {} ({})".format(i, slot_name, slot_type)
        if slot_rename:
            result_line += " - 别名: {}".format(slot_rename)
        
        formatted_results.append(result_line)
    
    return "\n".join(formatted_results)


if __name__ == "__main__":
    # 使用示例
    print("=== Slot Search Tool 使用示例 ===")
    
    try:
        # 示例 1: 搜索鲁迅
        slots = search_slots_with_match_phrase("鲁迅")
        result = format_slot_search_results(slots, "鲁迅")
        print("\n示例 1 - 搜索 '鲁迅':")
        print(result)
        
        # 示例 2: 搜索老舍
        slots = search_slots_with_match_phrase("老舍")
        print("\n示例 2 - 搜索 '老舍' (原始数据):")
        for i, slot in enumerate(slots, 1):
            print("{}. {} - 类型: {}".format(i, slot['slotName'], slot['slotType']))
        
        # 示例 3: 搜索不存在的槽位
        slots = search_slots_with_match_phrase("不存在的作者")
        result = format_slot_search_results(slots, "不存在的作者")
        print("\n示例 3 - 搜索不存在的槽位:")
        print(result)
        
    except Exception as e:
        print("执行搜索时出错: {}".format(str(e)))
        print("请确保 Elasticsearch 服务正在运行并且索引已创建。")