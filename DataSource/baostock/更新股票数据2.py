import baostock as bs
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import os
import sqlite3



_file_dir_ = os.path.split(os.path.realpath(__file__))[0] # 本文件的目录
DB_FILE_NAME = 'data.db'  # 数据库的文件
DB_FILE = os.path.join(_file_dir_, DB_FILE_NAME)

# 数据库部分
# 连接到 SQLite 数据库（如果不存在会自动创建）
conn = sqlite3.connect(DB_FILE)

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 这里要遍历所有的股票
# 获取行业分类数据
rs = bs.query_stock_industry()
print('query_stock_industry error_code:'+rs.error_code)
print('query_stock_industry respond  error_msg:'+rs.error_msg)
# 打印结果集
industry_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    industry_list.append(rs.get_row_data())
result = pd.DataFrame(industry_list, columns=rs.fields)
# 然后这里设置索引
result.set_index('code',inplace=True)
# 结果集输出到数据库,这里是替换的方式
result.to_sql('stock_industry', conn, if_exists='replace')
# 这里取得所有的额股票
codes = list(result.index) # 取得所有的股票名称

# 这里追加指数数据
dt_index=pd.read_excel(os.path.join(_file_dir_, '指数.xlsx'))
indexs = list(dt_index['指数代码'])

# 追加
codes.extend(indexs)


# 然后用进度条
for i  in tqdm(range(len(codes))):
    _code_name = codes[i]
    is_need_download_all = True
    # 下边判断是否只是更新部分

    # 判断是否需要下载全部
    if is_need_download_all:
        rs = bs.query_history_k_data_plus(
            _code_name,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            start_date='2010-01-01', # end_date='2021-12-21',
            frequency="d", adjustflag="1")
        # 保存在
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields) # 组成pd
        # 如下是转换数据类型
        result.loc[result['turn'] == '', 'turn'] = '0'
        result.loc[result['volume'] == '', 'volume'] = '0'
        result.loc[result['amount'] == '', 'amount'] = '0'
        result.loc[result['pctChg'] == '', 'pctChg'] = '0'
        result = result.astype(
            {
                'open':float,
                'high':float,
                'low':float,
                'close':float,
                'preclose':float,
                'volume':float,
                'amount':float,
                'turn':float,
                'pctChg':float,
                'adjustflag':int,
                'tradestatus':int,
                'isST':int,
            }
        )
        result['date']=pd.to_datetime(result['date'], format=f"%Y-%m-%d")
        result.set_index('date',inplace=True) # 设置索引
        # 输出到数据库
        result.to_sql(f'{_code_name}', conn, if_exists='replace') # 保存在数据库中

#### 登出系统 ####
bs.logout()