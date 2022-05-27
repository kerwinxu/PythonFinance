from os import sep
import baostock as bs
import pandas as pd
import os

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 这里先取得所有的股票
dt = pd.read_csv("stock_industry.csv", sep=',', encoding="gbk")

for i  in range(len(dt)):
    rs = bs.query_history_k_data_plus(dt.loc[i,'code'],
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
    start_date='2010-01-01', # end_date='2021-12-21',
    frequency="d", adjustflag="2")
    # 保存在
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    # 然后要保存在目录中。
    dest = os.path.join("k线数据", dt.loc[i,'code'] + ".csv")
    result.to_csv(dest, index=False)
    print("保存{},股票名称：{}".format(dt.loc[i,'code'], dt.loc[i,'code_name']))

#### 登出系统 ####
bs.logout()