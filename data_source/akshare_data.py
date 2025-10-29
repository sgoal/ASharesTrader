import akshare as ak
import pandas as pd

def get_fund_data(fund_code: str, start_date: str = None) -> pd.DataFrame:
    """
    Fetches fund data from Akshare.
    
    :param fund_code: The code of the fund.
    :param start_date: The start date in YYYYMMDD format.
    :return: A pandas DataFrame with the fund data.
    :raises Exception: If fetching data fails.
    """
    try:
        # The indicator "单位净值走势" gets the net asset value history.
        fund_data = ak.fund_open_fund_info_em(symbol=fund_code, indicator="单位净值走势")
        if fund_data.empty:
            raise ValueError("Akshare returned an empty DataFrame. The fund code might be incorrect or data is unavailable.")
        
        # Convert date column to datetime objects for comparison
        fund_data['净值日期'] = pd.to_datetime(fund_data['净值日期'])

        if start_date:
            # Filter the DataFrame based on the start_date
            start_datetime = pd.to_datetime(start_date, format='%Y%m%d')
            fund_data = fund_data[fund_data['净值日期'] >= start_datetime].reset_index(drop=True)

        return fund_data
    except Exception as e:
        # Include the original exception for better debugging
        raise Exception(f"Failed to fetch data for fund {fund_code}. Original error: {e}") from e