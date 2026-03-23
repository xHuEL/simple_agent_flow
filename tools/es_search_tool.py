from langchain_core.tools import tool
from common.es_client import create_es_client


@tool
def es_search_tool(query: str, index: str = "documents") -> str:
    """
    在 Elasticsearch 中执行全文搜索。
    
    该工具通过 Elasticsearch 搜索集群中的文档数据，支持全文检索和模糊匹配。
    适合用于搜索结构化数据、日志信息或内部知识库内容。

    Args:
        query: 搜索查询关键词，例如 "机器学习算法" 或 "系统错误日志"
        index: Elasticsearch 索引名称，默认为 "documents"

    Returns:
        一个字符串，包含搜索结果的摘要信息。
        如果搜索失败或无结果，返回友好的错误提示。
    """
    
    try:
        # 创建 ES 客户端实例
        es_client = create_es_client()
        
        # 执行搜索
        results = es_client.search(index=index, query=query, size=5)
        
        if not results:
            return "未找到相关结果。请尝试不同的搜索关键词。"
        
        # 格式化结果
        formatted_results = []
        for i, doc in enumerate(results, 1):
            # 提取文档的主要内容或标题和摘要
            title = doc.get('title', '无标题')
            content = doc.get('content', doc.get('text', '无内容'))
            
            # 限制内容长度
            if len(content) > 200:
                content = content[:200] + "..."
            
            formatted_results.append(f"{i}. {title}: {content}")
        
        return "\n".join(formatted_results)
        
    except Exception as e:
        return f"搜索执行失败: {str(e)}。请检查 Elasticsearch 连接配置。"