import importlib
from config import settings
from data_source.akshare_data import get_fund_data

class TraderAgent:
    """
    The AI trading agent, responsible for loading models, fetching data, and making decisions.
    """
    def __init__(self):
        self.models = self._load_models()
        self.fund_code = settings.DATA_SOURCE.get('fund_code')

    def _load_models(self):
        """Dynamically load and instantiate models from settings."""
        loaded_models = []
        for model_path in settings.MODELS:
            module_path, class_name = model_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            model_class = getattr(module, class_name)
            loaded_models.append(model_class())
        return loaded_models

    def run(self, data=None, current_shares: float = 0, cash: float = 0):
        """
        Executes the core logic of the agent: fetch data -> predict.
        If data is provided, it uses that data (for backtesting).
        Otherwise, it fetches new data.
        """
        fund_data = data
        if fund_data is None:
            if not self.fund_code:
                raise ValueError("Fund code not configured in settings.")
            # Fetch data
            fund_data = get_fund_data(fund_code=self.fund_code)

        # Execute each model and collect decisions
        decisions = {}
        for model in self.models:
            model_name = model.__class__.__name__
            decision = model.predict(fund_data, current_shares, cash)
            decisions[model_name] = decision
        
        return decisions