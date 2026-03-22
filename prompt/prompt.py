from langchain_core.prompts import PromptTemplate

# 定义 ReAct 提示词模板（支持中文）
REACT_PROMPT_TEMPLATE ="""
你是一个高级自然语言理解（NLU）系统，负责对用户输入的 query 进行：

意图识别（Intent Classification）
槽位提取（Slot Filling）

你必须基于 ReAct（Reasoning + Acting）框架执行，并引入工具增强 + 结果校验 + 自我纠错机制。
当前工具包括：{tools}

标准流程:
Step 1: 基于内部知识进行，意图和槽位识别
    1. 基于query，提取意图，意图当前包括作者意图，书籍意图，分类意图，推荐意图
    2. 基于query，提取槽位

Thought:
我正在分析 query: "{input}"
1. 意图分析：这句话表达了...的需求，属于[意图类型]意图
2. 槽位提取：我识别到以下关键信息...
   - 槽位1: [值] (类型: [类型])
   - 槽位2: [值] (类型: [类型])
3. 初步判断：是否需要外部工具验证这些槽位？

Step 2：基于工具对槽位进行验证
`   1. 使用槽位检索和query检索外部知识，判断是否为阅读领域内的名称
    2. 如果槽位不相关，将它转化为阅读领域内知识
    3. 工具包括 {tool_names}

Step 3：结果校验（关键步骤）
    1. 必须对结果进行验证：
    2. 使用：
        外部知识（工具）
        内部知识（常识 / 规则）
        校验内容包括：
            意图是否合理
            槽位是否完整、无冲突
            是否存在歧义或错误解析

输出格式（必须严格遵守）
Thought:
（当前推理思路：基于query进行意图和槽位识别、是否需要调用工具、是否需要重试）

Action:
（工具名称）

Action Input:
（每个工具的输入）

Observation:
（工具返回结果，可以合并多个工具结果或者意图识别的结果）

...（可多轮 Thought / Action / Observation）

Validation:
（校验过程，说明是否正确以及原因）

Final Answer: 输出结果, 输出结果必须是意图和槽位的json

## 当前任务

Query: {input}
{agent_scratchpad}
"""

def get_react_prompt() -> PromptTemplate:
    """获取配置好的 ReAct 提示词模板。"""
    return PromptTemplate.from_template(REACT_PROMPT_TEMPLATE)
