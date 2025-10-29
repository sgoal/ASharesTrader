# AI 基金交易 Agent 任务清单 (Phase 3)

## 阶段 1: 增强决策日志

- [ ] 修改 `models/base_model.py` 中 `predict` 方法的签名，使其返回 `tuple[str, str]` (decision, reason)。
- [ ] 在 `tests/test_models.py` 中更新 `SimpleModel` 和 `LLMModel` 的测试，以验证新的返回格式。
- [ ] 修改 `models/simple_model.py` 和 `models/llm_model.py` 以实现新的返回格式，包含决策理由。
- [ ] 修改 `trading_agent/agent.py` 和 `tests/test_agent.py` 以处理新的返回格式。
- [ ] 修改 `main.py` 以在 `run` 模式下打印决策及其理由。

## 阶段 2: 回测框架开发 (TDD)

- [ ] 创建 `backtester/__init__.py` 和 `tests/test_backtester.py`。
- [ ] 在 `tests/test_backtester.py` 中编写测试，模拟一个简单的策略回测场景，验证投资组合价值的计算。
- [ ] 创建 `backtester/backtester.py` 并实现 `Backtester` 类的最小化逻辑以通过测试。

## 阶段 3: 完整回测功能实现

- [ ] 完善 `Backtester` 类，使其能够处理真实的历史数据和交易逻辑。
- [ ] 在 `tests/test_backtester.py` 中添加更全面的测试，覆盖买入、卖出和持有操作。
- [ ] 完善 `Backtester` 的实现以通过所有测试。

## 阶段 4: 集成与运行

- [ ] 将 `argparse` 添加到 `main.py`，以支持 `run` 和 `backtest` 两个子命令。
- [ ] 将 `Backtester` 集成到 `main.py` 的 `backtest` 命令中。
- [ ] 运行 `main.py backtest` 进行端到端的回测，并打印最终的性能报告。