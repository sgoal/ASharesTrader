import sys
import pytest
import pandas as pd
from unittest.mock import MagicMock

# 将项目根目录添加到 Python 路径
sys.path.insert(0, '/Users/bytedance/agent/aitrade/ASharesTrader')

from backtester.backtester import Backtester

def test_backtester_simple_run():
    """
    测试回测器在一个简单的买入并持有场景下的行为。
    """
    # 准备: 模拟历史数据
    hist_data = pd.DataFrame({
        "净值日期": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
        "单位净值": [1.0, 1.1, 1.2]
    })

    # 准备: 模拟一个总是决定“买入”的 Agent
    mock_agent = MagicMock()
    # 第一次调用（在第二天），买入
    # 第二次调用（在第三天），持有（因为已经买了）
    mock_agent.run.side_effect = [
        {'MockModel': ('buy', 'reason')},
        {'MockModel': ('hold', 'reason')}
    ]

    # 执行回测
    backtester = Backtester(agent=mock_agent, initial_cash=1000)
    report = backtester.run(historical_data=hist_data)

    # 断言
    # 初始资金: 1000
    # 2023-01-02, 价格 1.1, 买入。花费 1000，获得 1000 / 1.1 = 909.09 份
    # 2023-01-03, 价格 1.2, 持有。投资组合价值 = 909.09 * 1.2 = 1090.90
    assert report['final_portfolio_value'] == pytest.approx(1090.91, 0.01)
    assert report['total_return_pct'] == pytest.approx(9.09, 0.01)

def test_backtester_buy_and_sell():
    """
    测试回测器在一个包含买入和卖出操作的场景下的行为。
    """
    # 准备: 历史数据
    hist_data = pd.DataFrame({
        "净值日期": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"]),
        "单位净值": [1.0, 1.1, 1.2, 1.15] # Day2买, Day3价值上升, Day4卖
    })

    # 准备: 模拟 Agent 决策
    mock_agent = MagicMock()
    mock_agent.run.side_effect = [
        {'MockModel': ('buy', 'reason')},   # Day 2: Buy
        {'MockModel': ('hold', 'reason')}, # Day 3: Hold
        {'MockModel': ('sell', 'reason')}  # Day 4: Sell
    ]

    # 执行
    backtester = Backtester(agent=mock_agent, initial_cash=1000)
    report = backtester.run(historical_data=hist_data)

    # 断言
    # Day 2 (Price 1.1): Buy 1000 / 1.1 = 909.09 shares. Cash = 0.
    # Day 3 (Price 1.2): Hold. Value = 909.09 * 1.2 = 1090.91
    # Day 4 (Price 1.15): Sell. Cash = 909.09 * 1.15 = 1045.45. Shares = 0.
    assert report['final_portfolio_value'] == pytest.approx(1045.45, 0.01)
    assert report['total_return_pct'] == pytest.approx(4.55, 0.01)
    assert len(report['trades']) == 2
    assert report['trades'][0]['action'] == 'buy'
    assert report['trades'][1]['action'] == 'sell'