import akshare as ak

stock_zh_a_hist_df = ak.stock_zh_a_daily(symbol="000001",  start_date="20170301", end_date='20240528', adjust="hfq")
print(stock_zh_a_hist_df)