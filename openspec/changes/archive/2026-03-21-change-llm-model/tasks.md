## 1. 配置文件与依赖准备

- [x] 1.1 创建 `config/.config` 示例文件，并包含 `KIMI_API_KEY=` 占位符
- [x] 1.2 确认 `langchain-openai` 已安装（用于兼容 Kimi 接口）

## 2. 核心逻辑修改

- [x] 2.1 在 `main.py` 中实现 `load_config(path)` 函数，用于从 `config/.config` 读取配置
- [x] 2.2 修改 `main.py` 的初始化逻辑，调用 `load_config` 并获取 `KIMI_API_KEY`
- [x] 2.3 在 `main.py` 中将 `ChatOpenAI` 的配置修改为 Kimi 的端点：`base_url="https://api.moonshot.cn/v1"`, `model="moonshot-v1-8k"`
- [x] 2.4 移除 `main.py` 中对 `.env` 加载 `OPENAI_API_KEY` 的逻辑

## 3. 验证与测试

- [x] 3.1 运行 `python3 main.py` 并手动输入 `config/.config` 路径（或使用默认路径）进行集成测试
- [x] 3.2 更新 `tests/test_agent.py` 中的 Mock 逻辑，确保兼容新的配置加载方式
- [x] 3.3 运行 `pytest tests/` 确保所有单元测试通过
