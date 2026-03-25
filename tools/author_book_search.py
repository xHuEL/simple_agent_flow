from langchain_core.tools import tool
from typing import Optional, Dict, List, Any
import json
from common.es_client import create_es_client

# 图书ID到书名的映射（snake_case到中文书名的映射）
BOOK_ID_TO_TITLE: Dict[str, str] = {
    "lu_xun_kuang_ren_ri_ji": "狂人日记",
    "lu_xun_a_q_zheng_zhuan": "阿Q正传",
    "lao_she_cha_guan": "茶馆",
    "lao_she_luo_tuo_xiang_zi": "骆驼祥子",
    "qian_zhong_shu_wei_cheng": "围城",
    "shen_cong_wen_bian_cheng": "边城",
    "zhang_ai_ling_qing_cheng_zli_lian": "倾城之恋",
    "mo_yan_hong_gao_liang_jia_zu": "红高粱家族",
    "yu_hua_huo_zhe": "活着",
    "lu_yao_ping_fan_de_shi_jie": "平凡的世界",
    "lev_tolstoy_war_and_peace": "战争与和平",
    "dostoevsky_crime_and_punishment": "罪与罚",
    "hemingway_the_old_man_and_the_sea": "老人与海",
    "george_orwell_1984": "1984",
    "jk_rowling_harry_potter": "哈利·波特与魔法石",
    "murakami_norwegian_wood": "挪威的森林",
    "higashino_naoya_miracles": "解忧杂货店",
    "marquez_one_hundred_years": "百年孤独",
    "hugo_les_miserables": "悲惨世界",
    "austen_pride_and_prejudice": "傲慢与偏见",
    "cao_xue_qin_dream_of_red_mansions": "红楼梦",
    "shi_nai_an_water_margin": "水浒传",
    "luo_guan_zhong_romance_of_three_kingdoms": "三国演义",
    "wu_cheng_en_journey_to_the_west": "西游记",
    "shakespeare_hamlet": "哈姆雷特",
    "dante_divine_comedy": "神曲",
    "o_henry_gift_of_magi": "The Gift of the Magi",
    "jose_saramago_blindness": "Blindness",
    "rabelais_gargantua": "Gargantua and Pantagruel",
    "emile_zola_germinal": "Germinal"
}


def get_book_title(book_id: str) -> str:
    """根据图书ID获取人类可读的书名"""
    return BOOK_ID_TO_TITLE.get(book_id, book_id)  # 如果找不到映射，返回原始ID


def build_search_query(search_config: Dict[str, Any]) -> Dict[str, Any]:
    """根据搜索配置构建Elasticsearch查询，使用should组合所有搜索类型"""
    query_text = search_config.get("query", "")
    fields = search_config.get("fields", ["slotName", "slotReName"])
    
    # 构建should查询，组合所有搜索类型
    should_queries = []
    
    # 1. 前缀搜索
    for field in fields:
        should_queries.append({"prefix": {field: query_text}})
    
    # 2. 全名匹配
    for field in fields:
        should_queries.append({"term": {field: query_text}})
    
    # 3. 包含搜索（模糊匹配）
    should_queries.append({
        "multi_match": {
            "query": query_text,
            "fields": [f"{field}^2.0" if field == "slotName" else f"{field}^1.0" for field in fields],
            "fuzziness": "AUTO",
            "type": "best_fields"
        }
    })
    
    return {
        "bool": {
            "should": should_queries,
            "minimum_should_match": 1  # 至少匹配一个should条件
        }
    }


@tool
def author_book_search_tool(search_config: str, index: str = "slots_index") -> str:
    """
    在 Elasticsearch 中执行作者-图书搜索，组合多种搜索方式。
    
    该工具专门用于搜索作者和图书的关联关系，同时使用前缀搜索、全名匹配和包含搜索。
    返回格式化的结果："作者名：xx，书名：xxx"

    Args:
        search_config: JSON格式的搜索配置，包含以下字段：
            - query: 搜索关键词
            - fields: 搜索字段列表（默认: ["slotName", "slotReName"]）
        index: Elasticsearch 索引名称，默认为 "slots_index"

    Returns:
        一个格式化字符串，包含作者名和书名信息。
        如果搜索失败或无结果，返回友好的错误提示。
    """
    
    try:
        # 解析JSON配置
        config = json.loads(search_config)
        query_text = config.get("query", "")
        
        if not query_text:
            return "搜索关键词不能为空"
        
        # 创建 ES 客户端实例
        es_client = create_es_client()
        
        # 构建搜索查询
        search_query = build_search_query(config)
        
        # 执行搜索，限制结果数量为10条
        results = es_client.search(index=index, query=search_query, size=10)
        
        if not results:
            return f"未找到与 '{query}' 相关的作者图书信息"
        
        # 格式化结果
        formatted_results = []
        for doc in results:
            author = doc.get('slotName', '未知作者')
            book_id = doc.get('slotReName', '未知书名')
            
            # 只返回包含有效作者和书名的结果
            if author != '未知作者' and book_id != '未知书名':
                book_title = get_book_title(book_id)
                formatted_results.append(f"作者名：{author}，书名：{book_title}")
        
        if not formatted_results:
            return f"未找到与 '{query}' 相关的作者图书信息"
        
        return "\n".join(formatted_results)
        
    except Exception as e:
        return f"搜索服务暂时不可用，请稍后重试。错误详情: {str(e)}"