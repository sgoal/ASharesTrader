import sys
import pytest
import pandas as pd
from unittest.mock import patch

# 将项目根目录添加到 Python 路径
sys.path.insert(0, '/Users/bytedance/agent/aitrade/ASharesTrader')

# 在我们创建相应的文件之前，下面的导入会失败
from data_source.akshare_data import get_fund_data

@patch('data_source.akshare_data.ak.fund_open_fund_info_em')
def test_get_fund_data_success(mock_akshare_call):
    """
    测试在 akshare 成功返回数据时 get_fund_data 的行为。
    """
    # 准备
    fund_code = "000001"
    expected_data = pd.DataFrame({
        "基金代码": [fund_code],
        "基金简称": ["测试基金"],
        "最新净值": [1.2345]
    })
    mock_akshare_call.return_value = expected_data

    # 执行
    data = get_fund_data(fund_code=fund_code)

    # 断言
    mock_akshare_call.assert_called_once_with(symbol=fund_code, indicator="单位净值走势")
    pd.testing.assert_frame_equal(data, expected_data)

@patch('data_source.akshare_data.ak.fund_open_fund_info_em')
def test_get_fund_data_akshare_error(mock_akshare_call):
    """
    测试在 akshare 抛出异常时 get_fund_data 的行为。
    """
    # 准备
    fund_code = "999999"
    mock_akshare_call.side_effect = Exception("Failed to fetch data")

    # 执行并断言
    with pytest.raises(Exception, match="Original error: Failed to fetch data"):
        get_fund_data(fund_code=fund_code)
    
    mock_akshare_call.assert_called_once_with(symbol=fund_code, indicator="单位净值走势")