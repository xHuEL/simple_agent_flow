import os
import sys
import argparse
from langchain_openai import ChatOpenAI
from tools.search import search_tool
from tools.es_search_tool import es_search_tool
from prompt.prompt import get_react_prompt
from agent.agent import create_agent, run_agent


def load_config(path: str) -> dict:
    """从指定路径加载配置信息。"""
    config = {}
    if not os.path.exists(path):
        return config
    
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config

def main():
    # 1. 解析命令行参数
    
    parser = argparse.ArgumentParser(description="ReAct 智能体系统")
    parser.add_argument("--config", type=str, default="config/.config", help="配置文件路径")
    args = parser.parse_args()

    # 2. 加载配置文件
    config = load_config(args.config)
    kimi_api_key = config.get("KIMI_API_KEY")

    if not kimi_api_key:
        print(f"错误: 请在 {args.config} 文件中设置 KIMI_API_KEY。")
        sys.exit(1)
        
    print(kimi_api_key)

    # 3. 初始化 Kimi LLM (通过 OpenAI 兼容接口) 和工具
    llm = ChatOpenAI(
        model="moonshot-v1-8k",  # 或 "moonshot-v1-32k", "moonshot-v1-128k"
        openai_api_key=kimi_api_key,  # 替换成你的真实 Key
        base_url="https://api.moonshot.cn/v1",   # Kimi的API地址
        temperature=0.7,                         # 控制随机性
        max_tokens=1024,    
    )

    tools = [search_tool, es_search_tool]
    
    # 3. 获取提示词模板并构建智能体
    prompt = get_react_prompt()
    agent = create_agent(model=llm, tools=tools, system_prompt = prompt)
    
    run_agent(agent, tools=tools, max_iterations=5, query="郭靖与黄蓉")

if __name__ == "__main__":
    main()