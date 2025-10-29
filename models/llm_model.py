import pandas as pd
from openai import OpenAI
from typing import Tuple
from models.base_model import BaseModel
from config import settings
from data_source.akshare_data import get_fund_basic_info, get_fund_portfolio_changes, get_fund_manager_changes

class LLMModel(BaseModel):
    """
    A model that uses a Deepseek/OpenAI compatible LLM for trading decisions.
    """
    def __init__(self):
        if not settings.DEEPSEEK_API_KEY:
            raise ValueError("Deepseek API key not found in settings.")
        
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_API_BASE
        )
        self.model_name = settings.DEEPSEEK_API_MODEL

    def predict(self, data: pd.DataFrame, fund_code: str, current_date: pd.Timestamp, current_shares: float = 0, cash: float = 0) -> Tuple[str, str]:
        """
        Sends financial data and portfolio status to the LLM and parses its decision.
        """
        if data.empty:
            return 'hold', "Insufficient data to make a decision."

        # Use tools to get more info
        fund_info = get_fund_basic_info(fund_code)
        portfolio_changes = get_fund_portfolio_changes(fund_code, current_date)
        manager_changes = get_fund_manager_changes(fund_code, current_date)

        # Build the prompt
        prompt = self._build_prompt(data, fund_info, portfolio_changes, manager_changes, current_shares, cash)

        # Call the API
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst. Based on the provided fund data and current portfolio, make a decision of 'buy', 'sell', or 'hold'. Provide a brief, one-sentence reason for your decision. Your entire response must be a single line of text in the format: DECISION | REASON"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150, # Increased tokens for more detailed reasons
                temperature=0.7,
            )
            raw_response = response.choices[0].message.content.strip()
            
            # Parse the response
            if '|' in raw_response:
                decision, reason = raw_response.split('|', 1)
                decision = decision.lower().strip()
                reason = reason.strip()
                if decision in ['buy', 'sell', 'hold']:
                    return decision, reason
            
            # If parsing fails, return hold with the raw response as the reason
            return 'hold', f"LLM returned an unparsable response: '{raw_response}'"

        except Exception as e:
            return 'hold', f"Error calling API: {e}"

    def _build_prompt(self, data: pd.DataFrame, fund_info, portfolio_changes, manager_changes, current_shares: float, cash: float) -> str:
        """Builds the prompt for the LLM based on the data and portfolio."""
        recent_data = data.tail(10).to_string()
        portfolio_status = f"Current Holdings: {current_shares:,.2f} shares, Current Cash: ${cash:,.2f}"
        fund_info_str = fund_info.to_string() if isinstance(fund_info, pd.DataFrame) else str(fund_info)
        portfolio_changes_str = portfolio_changes.to_string() if isinstance(portfolio_changes, pd.DataFrame) else str(portfolio_changes)
        manager_changes_str = manager_changes.to_string() if isinstance(manager_changes, pd.DataFrame) else str(manager_changes)

        return f"""{portfolio_status}

**Fund Information:**
{fund_info_str}

**Recent Portfolio Changes (Buy):**
{portfolio_changes_str}

**Recent Manager Changes:**
{manager_changes_str}

**Recent Fund Net Value Data:**
{recent_data}

Please analyze all the above information and provide your trading recommendation in the format: DECISION | REASON"""