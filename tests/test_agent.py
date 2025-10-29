import sys
import pytest
from unittest.mock import patch, MagicMock

from trading_agent.agent import TraderAgent

# 将项目根目录添加到 Python 路径
sys.path.insert(0, '/Users/bytedance/agent/aitrade/ASharesTrader')

# We have to mock the class within the module where it is imported.
@patch('trading_agent.agent.settings')
@patch('models.simple_model.SimpleModel')
def test_agent_initialization(MockSimpleModel, mock_settings):
    """测试 TraderAgent 的初始化过程。"""
    mock_settings.MODELS = ['models.simple_model.SimpleModel']
    mock_settings.DATA_SOURCE = {'fund_code': '000001'}
    
    agent = TraderAgent()
    # 验证模型是否被正确加载
    assert len(agent.models) == 1
    # 验证数据源配置是否被正确加载
    assert agent.fund_code == '000001'

@patch('trading_agent.agent.settings')
@patch('trading_agent.agent.get_fund_net_value_history')
@patch('models.simple_model.SimpleModel')
def test_agent_run_with_fetch(MockSimpleModel, mock_get_fund_data, mock_settings):
    """测试 TraderAgent 在需要自己获取数据时的逻辑。"""
    # 准备
    mock_settings.MODELS = ['models.simple_model.SimpleModel']
    mock_settings.DATA_SOURCE = {'fund_code': '000001'}
    mock_get_fund_data.return_value = "some fund data"
    mock_model_instance = MockSimpleModel.return_value
    mock_model_instance.__class__.__name__ = 'SimpleModel'
    mock_model_instance.predict.return_value = ('buy', 'Simple reason')

    agent = TraderAgent()

    # 执行
    decisions = agent.run()

    # 断言
    mock_get_fund_data.assert_called_once_with(fund_code='000001')
    mock_model_instance.predict.assert_called_once()
    # We can't easily assert the timestamp, so we check the other args
    call_args = mock_model_instance.predict.call_args[0]
    assert call_args[0] == "some fund data"
    assert call_args[1] == "000001"
    assert call_args[3] == 0 # current_shares
    assert call_args[4] == 0 # cash
    assert decisions == {'SimpleModel': ('buy', 'Simple reason')}

@patch('trading_agent.agent.settings')
@patch('models.simple_model.SimpleModel')
def test_agent_run_with_provided_data(MockSimpleModel, mock_settings):
    """测试 TraderAgent 在被提供了数据时的逻辑（回测场景）。"""
    mock_settings.MODELS = ['models.simple_model.SimpleModel']
    mock_settings.DATA_SOURCE = {'fund_code': '000001'}
    mock_model_instance = MockSimpleModel.return_value
    mock_model_instance.__class__.__name__ = 'SimpleModel'
    mock_model_instance.predict.return_value = ('buy', 'Simple reason')

    agent = TraderAgent()
    # 执行
    decisions = agent.run(data="provided data")
    # 断言
    call_args = mock_model_instance.predict.call_args[0]
    assert call_args[0] == "provided data"
    assert call_args[1] == "000001"
    assert call_args[3] == 0 # current_shares
    assert call_args[4] == 0 # cash
    assert decisions == {'SimpleModel': ('buy', 'Simple reason')}