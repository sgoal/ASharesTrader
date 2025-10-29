import pandas as pd
import akshare as ak

def get_fund_net_value_history(fund_code: str, start_date: str = None) -> pd.DataFrame:
    """Fetches fund net value history from Akshare."""
    try:
        fund_data = ak.fund_open_fund_info_em(symbol=fund_code, indicator="单位净值走势")
        if fund_data.empty:
            raise ValueError("Akshare returned an empty DataFrame for net value history.")
        
        fund_data['净值日期'] = pd.to_datetime(fund_data['净值日期'])

        if start_date:
            start_datetime = pd.to_datetime(start_date, format='%Y%m%d')
            fund_data = fund_data[fund_data['净值日期'] >= start_datetime].reset_index(drop=True)

        return fund_data
    except Exception as e:
        raise Exception(f"Failed to fetch net value history for fund {fund_code}. Original error: {e}") from e

def get_fund_basic_info(fund_code: str) -> pd.DataFrame:
    """Fetches basic fund information from Akshare."""
    try:
        info_df = ak.fund_open_fund_info_em(symbol=fund_code)
        if info_df.empty:
            raise ValueError("Akshare returned an empty DataFrame for basic info.")
        return info_df
    except Exception as e:
        raise Exception(f"Failed to fetch basic info for fund {fund_code}. Original error: {e}") from e

def get_fund_portfolio_changes(fund_code: str, date: pd.Timestamp) -> pd.DataFrame:
    """Fetches recent portfolio changes for a fund up to a given date."""
    try:
        # Fetch changes for the year of the given date
        year = date.year
        buy_changes = ak.fund_portfolio_change_em(symbol=fund_code, indicator="累计买入", date=str(year))
        # For simplicity, we only consider buy changes in the prompt
        if buy_changes.empty:
            return pd.DataFrame([{"info": f"No portfolio changes found for {year}."}])
        return buy_changes
    except Exception as e:
        return pd.DataFrame([{"error": f"Could not retrieve portfolio changes: {e}"}])

def get_fund_manager_changes(fund_code: str, date: pd.Timestamp) -> pd.DataFrame:
    """Fetches personnel changes for a fund up to a given date."""
    try:
        manager_changes = ak.fund_announcement_personnel_em(symbol=fund_code)
        if manager_changes.empty:
            return pd.DataFrame([{"info": "No personnel changes found."}])
        
        # Filter announcements up to the decision date
        manager_changes['公告日期'] = pd.to_datetime(manager_changes['公告日期'])
        return manager_changes[manager_changes['公告日期'] <= date]
    except Exception as e:
        return pd.DataFrame([{"error": f"Could not retrieve manager changes: {e}"}])