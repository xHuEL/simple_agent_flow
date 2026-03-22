import requests
import json

from langchain_core.tools import tool

@tool
def search_tool(query: str) -> str:
    """
    联网搜索获取相关知识。

    该工具通过 Bocha 搜索 API 获取与查询相关的网页摘要片段。
    适合用于获取实时信息、事实查询或背景知识。

    Args:
        query: 查询关键词，例如 "斗罗大陆和凡人修仙的关系" 或 "凡人修仙传的作者"

    Returns:
        一个字符串，包含最多 10 条搜索结果的摘要片段，
        每条结果以 "• " 开头并换行分隔。
        如果搜索失败或无结果，返回友好的错误提示。
    """

    url = "https://api.bocha.cn/v1/web-search"

    payload = json.dumps({
        "query": query,
        "summary": True,
        "count": 10
    })

    headers = {
        'Authorization': 'Bearer sk-be262cc8c44e463e97db94add1ff26e2',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_str = json.dumps(response.json())  # 对象转字符串
    json_data = json.loads(json_str)  # 字符串转对象
    result = []
    values = json_data['data']['webPages']['value']
    for value in values:
        result.append(value['snippet'])

    return str(result)