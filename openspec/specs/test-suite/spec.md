## ADDED Requirements

### Requirement: 工具单元测试
系统 MUST 为所有工具提供单元测试，使用 `pytest` 进行验证。

#### Scenario: 成功运行工具测试
- **WHEN** 运行 `pytest tests/test_tools.py`
- **THEN** 所有针对 `search.py` 和 `wikipedia.py` 的测试均通过。

### Requirement: 智能体构建和执行测试
系统 MUST 为智能体的构建和执行逻辑提供单元测试，并使用 `unittest.mock` 对 LLM 调用进行模拟。

#### Scenario: 成功运行智能体测试
- **WHEN** 运行 `pytest tests/test_agent.py`
- **THEN** 验证 `builder.py` 和 `executor.py` 的逻辑正确，且不实际调用真实的 LLM 接口。
