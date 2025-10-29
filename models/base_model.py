from abc import ABC, abstractmethod
import pandas as pd
from typing import Tuple

class BaseModel(ABC):
    """
    The abstract base class for all trading models.
    """
    @abstractmethod
    def predict(self, data: pd.DataFrame, fund_code: str, current_date: pd.Timestamp, current_shares: float = 0, cash: float = 0) -> Tuple[str, str]:
        """
        Makes a trading prediction based on the input data and current portfolio.

        :param data: A pandas DataFrame containing market data.
        :param fund_code: The fund code being analyzed.
        :param current_date: The date of the decision, for point-in-time data retrieval.
        :param current_shares: The number of shares currently held.
        :param cash: The amount of cash currently available.
        :return: A tuple containing the trading signal ('buy', 'sell', or 'hold') and the reason for the decision.
        """
        pass