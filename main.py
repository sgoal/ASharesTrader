import sys
import argparse

# 将项目根目录添加到 Python 路径
sys.path.insert(0, '/Users/bytedance/agent/aitrade/ASharesTrader')

from trading_agent.agent import TraderAgent
from backtester.backtester import Backtester
from data_source.akshare_data import get_fund_data

def run_live(agent):
    """运行实时决策模式。"""
    print("\nRunning agent to get live trading decisions...")
    decisions = agent.run()
    
    print("\n--- Trading Decisions ---")
    for model_name, (decision, reason) in decisions.items():
        print(f"- Model '{model_name}': {decision.upper()}")
        print(f"  Reason: {reason}")
    print("-------------------------\n")

from datetime import datetime, timedelta

from report.generator import generate_html_report

def run_backtest(agent, start_date_str):
    """运行历史回测模式。"""
    if start_date_str:
        start_date = start_date_str
    else:
        # 默认回测最近半年
        start_date = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')

    print(f"\nFetching historical data for fund {agent.fund_code} from {start_date}...")
    # 获取完整的历史数据用于回测
    historical_data = get_fund_data(fund_code=agent.fund_code, start_date=start_date)
    print(f"Found {len(historical_data)} data points.")

    print("Running backtest...")
    backtester = Backtester(agent=agent, initial_cash=10000.0)
    report = backtester.run(historical_data=historical_data)

    print("\n--- Backtest Report ---")
    print(f"Initial Portfolio Value: ${backtester.initial_cash:,.2f}")
    print(f"Final Portfolio Value:   ${report['final_portfolio_value']:,.2f}")
    print(f"Total Return:              {report['total_return_pct']:.2f}%")
    print(f"Total Trades:              {len(report['trades'])}")
    print("-----------------------\n")

    # 生成HTML报告
    generate_html_report(report)

def main():
    """
    应用程序主入口，处理命令行参数。
    """
    parser = argparse.ArgumentParser(description="AI Trading Agent")
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # 定义 run 命令
    parser_run = subparsers.add_parser('run', help='Get live trading decisions.')

    # 定义 backtest 命令
    parser_backtest = subparsers.add_parser('backtest', help='Run a backtest on historical data.')
    parser_backtest.add_argument('--start', type=str, help='Start date for backtesting in YYYYMMDD format.')

    args = parser.parse_args()

    print("Initializing AI Trading Agent...")
    try:
        agent = TraderAgent()
        print(f"Loaded {len(agent.models)} model(s).")
        print(f"Target fund code: {agent.fund_code}")

        if args.command == 'run':
            run_live(agent)
        elif args.command == 'backtest':
            run_backtest(agent, args.start)

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your configuration and network connection.")

if __name__ == "__main__":
    main()