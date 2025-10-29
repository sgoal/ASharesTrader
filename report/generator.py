import json

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backtest Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: sans-serif; margin: 2rem; background-color: #f4f4f9; color: #333; }
        h1 { color: #1a1a1a; }
        #chart-container { max-width: 900px; margin: 2rem 0; background-color: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <h1>Backtest Report</h1>
    <div id="chart-container">
        <canvas id="portfolio-chart"></canvas>
    </div>
    <script>
        const backtestData = {backtest_data};
    </script>
    <script src="static/index.js"></script>
</body>
</html>
"""

def generate_html_report(report_data, output_path="report/backtest_report.html"):
    """Generates an HTML report from the backtest data."""
    # Convert datetime objects to string for JSON serialization
    for item in report_data['history']:
        item['date'] = item['date'].strftime('%Y-%m-%d')
    for trade in report_data['trades']:
        trade['date'] = trade['date'].strftime('%Y-%m-%d')

    # Inject data into the template
    html_content = HTML_TEMPLATE.replace("{backtest_data}", json.dumps(report_data))

    # Write to file
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    print(f"\nSuccessfully generated report at: {output_path}")