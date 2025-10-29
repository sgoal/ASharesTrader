import sys
import pytest
import pandas as pd

# 将项目根目录添加到 Python 路径
sys.path.insert(0, '/Users/bytedance/agent/aitrade/ASharesTrader')

from models.simple_model import SimpleModel

def test_simple_model_predict_buy():
    """测试 SimpleModel 在价格上涨时返回 'buy'。"""
    model = SimpleModel()
    data = pd.DataFrame({
        "净值日期": pd.to_datetime(["2023-01-01", "2023-01-02"]),
        "单位净值": [1.0, 1.1]
    })
    decision, reason = model.predict(data, fund_code="000001", current_date=pd.Timestamp.now())
    assert decision == 'buy'
    assert isinstance(reason, str)

def test_simple_model_predict_sell():
    """测试 SimpleModel 在价格下跌时返回 'sell'。"""
    model = SimpleModel()
    data = pd.DataFrame({
        "净值日期": pd.to_datetime(["2023-01-01", "2023-01-02"]),
        "单位净值": [1.1, 1.0]
    })
    decision, reason = model.predict(data, fund_code="000001", current_date=pd.Timestamp.now())
    assert decision == 'sell'
    assert isinstance(reason, str)

def test_simple_model_predict_hold():
    """测试 SimpleModel 在价格不变时返回 'hold'。"""
    model = SimpleModel()
    data = pd.DataFrame({
        "净值日期": pd.to_datetime(["2023-01-01", "2023-01-02"]),
        "单位净值": [1.0, 1.0]
    })
    decision, reason = model.predict(data, fund_code="000001", current_date=pd.Timestamp.now())
    assert decision == 'hold'
    assert isinstance(reason, str)

from unittest.mock import patch, MagicMock
from models.llm_model import LLMModel

@patch('models.llm_model.get_fund_manager_changes')
@patch('models.llm_model.get_fund_portfolio_changes')
@patch('models.llm_model.get_fund_basic_info')
@patch('models.llm_model.OpenAI')
def test_llm_model_predict_buy(MockOpenAIClient, mock_get_info, mock_get_portfolio, mock_get_manager):
    """测试 LLMModel 在 API 返回 'buy' 时正确解析。"""
    # 准备
    decision_date = pd.Timestamp.now()
    mock_client_instance = MockOpenAIClient.return_value
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "buy | The trend is upward."
    mock_client_instance.chat.completions.create.return_value = mock_response
    mock_get_info.return_value = "Mocked fund info"
    mock_get_portfolio.return_value = "Mocked portfolio changes"
    mock_get_manager.return_value = "Mocked manager changes"

    model = LLMModel()
    data = pd.DataFrame({
        "净值日期": pd.to_datetime(["2023-01-01", "2023-01-02"]),
        "单位净值": [1.0, 1.1]
    })

    # 执行
    decision, reason = model.predict(data, fund_code="000001", current_date=decision_date, cash=1000, current_shares=0)

    # 断言
    assert decision == 'buy'
    assert reason == "The trend is upward."
    mock_client_instance.chat.completions.create.assert_called_once()
    mock_get_info.assert_called_once_with("000001")
    mock_get_portfolio.assert_called_once_with("000001", decision_date)
    mock_get_manager.assert_called_once_with("000001", decision_date)

def test_simple_model_insufficient_data():
    """测试 SimpleModel 在数据不足时返回 'hold'。"""
    model = SimpleModel()
    data = pd.DataFrame({
        "净值日期": pd.to_datetime(["2023-01-01"]),
        "单位净值": [1.0]
    })
    decision, reason = model.predict(data, fund_code="000001", current_date=pd.Timestamp.now())
    assert decision == 'hold'
    assert isinstance(reason, str)

def test_simple_model_empty_data():
    """测试 SimpleModel 在数据为空时返回 'hold'。"""
    model = SimpleModel()
    data = pd.DataFrame()
    decision, reason = model.predict(data, fund_code="000001", current_date=pd.Timestamp.now())
    assert decision == 'hold'
    assert isinstance(reason, str)