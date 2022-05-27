import pandas as pd


dt = dt = pd.read_csv("stock_industry.csv", sep=',', encoding="gbk")

for i  in range(len(dt)):
    print(dt.loc[i, 'code'])
