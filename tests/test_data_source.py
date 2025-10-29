import sys
import pytest
import pandas as pd
from unittest.mock import patch

# 将项目根目录添加到 Python 路径
sys.path.insert(0, '/Users/bytedance/agent/aitrade/ASharesTrader')

from data_source.akshare_data import get_fund_net_value_history, get_fund_basic_info, get_fund_portfolio_changes, get_fund_manager_changes

@patch('data_source.akshare_data.ak.fund_open_fund_info_em')
def test_get_fund_net_value_history_success(mock_akshare_call):
    """测试在 akshare 成功返回数据时 get_fund_net_value_history 的行为。"""
    # 准备
    fund_code = "000001"
    expected_data = pd.DataFrame({
        "净值日期": pd.to_datetime(["2023-01-01"]),
        "基金代码": [fund_code],
        "基金简称": ["测试基金"],
        "最新净值": [1.2345]
    })
    mock_akshare_call.return_value = expected_data

    # 执行
    data = get_fund_net_value_history(fund_code=fund_code)

    # 断言
    mock_akshare_call.assert_called_once_with(symbol=fund_code, indicator="单位净值走势")
    pd.testing.assert_frame_equal(data, expected_data)

@patch('data_source.akshare_data.ak.fund_open_fund_info_em')
def test_get_fund_net_value_history_error(mock_akshare_call):
    """测试在 akshare 抛出异常时 get_fund_net_value_history 的行为。"""
    # 准备
    fund_code = "999999"
    mock_akshare_call.side_effect = Exception("Failed to fetch data")

    # 执行并断言
    with pytest.raises(Exception, match="Original error: Failed to fetch data"):
        get_fund_net_value_history(fund_code=fund_code)
    
    mock_akshare_call.assert_called_once_with(symbol=fund_code, indicator="单位净值走势")

@patch('data_source.akshare_data.ak.fund_open_fund_info_em')
def test_get_fund_basic_info_success(mock_akshare_call):
    """测试 get_fund_basic_info 在成功时返回数据。"""
    # 准备
    fund_code = "000001"
    expected_info = pd.DataFrame([{"item": "基金全称", "value": "华夏成长混合"}])
    mock_akshare_call.return_value = expected_info

    # 执行
    info = get_fund_basic_info(fund_code=fund_code)

    # 断言
    mock_akshare_call.assert_called_once_with(symbol=fund_code)
    pd.testing.assert_frame_equal(info, expected_info)

@patch('data_source.akshare_data.ak.fund_portfolio_change_em')
def test_get_fund_portfolio_changes(mock_akshare_call):
    """测试 get_fund_portfolio_changes 函数。"""
    mock_akshare_call.return_value = pd.DataFrame([{"stock": "AAPL"}])
    get_fund_portfolio_changes("000001", pd.Timestamp.now())
    assert mock_akshare_call.call_count == 1

@patch('data_source.akshare_data.ak.fund_announcement_personnel_em')
def test_get_fund_manager_changes(mock_akshare_call):
    """测试 get_fund_manager_changes 函数。"""
    mock_akshare_call.return_value = pd.DataFrame({
        "公告日期": pd.to_datetime(["2023-01-01", "2024-01-01"]),
        "manager": ["Old Guy", "New Guy"]
    })
    result = get_fund_manager_changes("000001", pd.to_datetime("2023-06-01"))
    mock_akshare_call.assert_called_once_with(symbol="000001")
    assert len(result) == 1
    assert result.iloc[0]['manager'] == 'Old Guy'