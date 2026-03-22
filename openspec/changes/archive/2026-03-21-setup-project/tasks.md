## 1. 基础环境搭建

- [x] 1.1 创建核心目录结构：`tools/`, `prompt/`, `agent/`, `tests/`
- [x] 1.2 创建配置文件：`requirements.txt` (添加 langchain, openai, pytest 等), `.env.example`
- [x] 1.3 初始化 `tests/__init__.py` 和 `tests/conftest.py`

## 2. 工具层实现

- [x] 2.1 实现 `tools/search.py`: 使用 `@tool` 定义 Web 搜索工具 (需要外部 API 访问)
- [x] 2.2 实现 `tools/wikipedia.py`: 使用 `@tool` 定义 Wikipedia 检索工具 (需要外部 API 访问)

## 3. 提示词与智能体层实现

- [x] 3.1 实现 `prompt/react_prompt.py`: 定义支持中文的 ReAct 提示词模板
- [x] 3.2 实现 `agent/builder.py`: 封装 `create_react_agent` 逻辑
- [x] 3.3 实现 `agent/executor.py`: 封装 `AgentExecutor` 并支持流式输出

## 4. 入口与测试

- [x] 4.1 实现 `main.py`: 支持命令行交互输入和智能体执行
- [x] 4.2 编写 `tests/test_tools.py`: 验证工具的输入输出和异常处理
- [x] 4.3 编写 `tests/test_prompt.py`: 验证提示词模板的格式 and 动态注入
- [x] 4.4 编写 `tests/test_agent.py`: 模拟 LLM 调用，验证智能体构建和执行逻辑
