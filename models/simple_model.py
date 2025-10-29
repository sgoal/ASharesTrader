import pandas as pd
from models.base_model import BaseModel

from typing import Tuple

class SimpleModel(BaseModel):
    """
    A simple trading model based on the change of the last two net asset values.
    """
    def predict(self, data: pd.DataFrame, fund_code: str, current_date: pd.Timestamp, current_shares: float = 0, cash: float = 0) -> Tuple[str, str]:
        """
        If there are fewer than 2 data points, returns 'hold'.
        Otherwise, compares the last two net asset values:
        - If the latest value > previous value, returns 'buy'.
        - If the latest value < previous value, returns 'sell'.
        - If they are equal, returns 'hold'.
        """
        if data.empty or len(data) < 2:
            return 'hold', "Insufficient data to make a decision."

        # Ensure data is sorted by date
        data = data.sort_values(by='净值日期').reset_index(drop=True)

        latest_value = data['单位净值'].iloc[-1]
        previous_value = data['单位净值'].iloc[-2]

        if latest_value > previous_value:
            reason = f"Price increased from {previous_value:.4f} to {latest_value:.4f}."
            return 'buy', reason
        elif latest_value < previous_value:
            reason = f"Price decreased from {previous_value:.4f} to {latest_value:.4f}."
            return 'sell', reason
        else:
            return 'hold', f"Price remained unchanged at {latest_value:.4f}."