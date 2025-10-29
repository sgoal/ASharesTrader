import akshare as ak
import pandas as pd

def get_fund_data(fund_code: str, start_date: str = None) -> pd.DataFrame:
    """
    Fetches fund data from Akshare.
    
    :param fund_code: The code of the fund.
    :return: A pandas DataFrame with the fund data.
    :raises Exception: If fetching data fails.
    """
    try:
        # Using fund_open_fund_info_em as decided in the test.
        # The indicator "单位净值走势" seems appropriate for getting historical data.
        fund_data = ak.fund_open_fund_info_em(symbol=fund_code, indicator="单位净值走势")
        if fund_data.empty:
            raise ValueError("Akshare returned an empty DataFrame. The fund code might be incorrect or data is unavailable.")
        return fund_data
    except Exception as e:
        # The test expects a specific error message format
        raise Exception(f"Failed to fetch data for fund {fund_code}. Original error: {e}") from e