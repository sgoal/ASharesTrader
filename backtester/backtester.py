import pandas as pd

class Backtester:
    def __init__(self, agent, initial_cash=10000.0):
        self.agent = agent
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.shares = 0.0
        self.portfolio_value = initial_cash
        self.trades = []

    def run(self, historical_data: pd.DataFrame):
        # 确保数据按日期排序
        data = historical_data.sort_values(by='净值日期').reset_index(drop=True)

        # 从第二天开始迭代，因为我们需要前一天的数据来做决策
        for i in range(1, len(data)):
            current_date = data['净值日期'].iloc[i]
            current_price = data['单位净值'].iloc[i]
            
            # 提供给 agent 的是截止到“今天”之前的所有数据
            agent_data = data.iloc[:i]
            
            # 获取 agent 的决策
            # 我们只关心第一个模型的决策来简化逻辑
            decisions = self.agent.run(data=agent_data, current_shares=self.shares, cash=self.cash)
            main_decision, reason = list(decisions.values())[0]

            # 执行交易
            shares_traded = 0
            if main_decision == 'buy' and self.cash > 0:
                shares_to_buy = self.cash / current_price
                self.shares += shares_to_buy
                self.cash = 0
                shares_traded = shares_to_buy
                self.trades.append({
                    'date': current_date,
                    'action': 'buy',
                    'price': current_price,
                    'shares': shares_to_buy
                })
            elif main_decision == 'sell' and self.shares > 0:
                self.cash += self.shares * current_price
                sold_shares = self.shares
                self.shares = 0
                shares_traded = sold_shares
                self.trades.append({
                    'date': current_date,
                    'action': 'sell',
                    'price': current_price,
                    'shares': sold_shares
                })
            
            # 更新当前投资组合总价值
            self.portfolio_value = self.cash + self.shares * current_price

            # 打印本轮日志
            print(f"--- {current_date} ---")
            print(f"Decision: {main_decision.upper()} ({reason})")
            if shares_traded > 0:
                print(f"  Action: {main_decision.upper()} {shares_traded:,.2f} shares @ ${current_price:,.2f}")
            print(f"  Portfolio Value: ${self.portfolio_value:,.2f} (Cash: ${self.cash:,.2f}, Shares: {self.shares:,.2f})")

        # 生成报告
        total_return = self.portfolio_value - self.initial_cash
        total_return_pct = (total_return / self.initial_cash) * 100

        report = {
            "final_portfolio_value": self.portfolio_value,
            "total_return_pct": total_return_pct,
            "trades": self.trades
        }
        return report