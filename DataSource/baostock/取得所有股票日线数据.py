from os import sep
import baostock as bs
import pandas as pd
import os
from datetime import datetime
from tqdm import tqdm

_file_path_ = os.path.split(os.path.realpath(__file__))[0]

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)


def download_data():
    # 索取所有的股票。
    # 先取得交易日
    rs = bs.query_trade_dates(start_date="2017-01-01", end_date=datetime.now().strftime(r'%Y-%m-%d'))
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    _date = data_list[-2][0]
    stock_rs = bs.query_all_stock(_date)
    stock_df = stock_rs.get_data()
    _codes = list(stock_df["code"])
    return _codes

# 这里先取得所有的股票
# dt = pd.read_csv("stock_industry.csv", sep=',', encoding="gbk")
# 先取得当前日期的所有股票的数据
_codes = download_data()



for i  in tqdm(range(len(_codes))):
    rs = bs.query_history_k_data_plus(_codes[i],
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
    dest = os.path.join(_file_path_, "k线数据", _codes[i] + ".csv")
    result.to_csv(dest, index=False,encoding='utf_8_sig')
    # print("保存{},股票名称：{}".format(dt.loc[i,'code'], dt.loc[i,'code_name']))

#### 登出系统 ####
bs.logout()