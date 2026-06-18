# 这个文件是将csv文件转成sqlite文件

import pandas as pd
from datetime import datetime
from tqdm import tqdm
import os
import sqlite3

_file_dir_ = os.path.split(os.path.realpath(__file__))[0] # 本文件的目录
DB_FILE_NAME = 'data.db'  # 数据库的文件
DB_FILE = os.path.join(_file_dir_, DB_FILE_NAME)
# 这里先删除这个数据库
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

# 数据库部分
# 连接到 SQLite 数据库（如果不存在会自动创建）
conn = sqlite3.connect(DB_FILE)

# 先取得有多少支股票
dt_a = pd.read_csv(os.path.join(_file_dir_, 'stock_industry.csv'),encoding='utf-8')
codes = list(dt_a['code']) # 取得所有的A股票名称
dt_a.set_index('code',inplace=True) # 设置索引
dt_a.to_sql('stock_industry',  conn, if_exists='replace')

# 这里追加指数数据
dt_index=pd.read_excel(os.path.join(_file_dir_, '指数.xlsx'))
indexs = list(dt_index['指数代码'])
dt_index.set_index('指数代码',inplace=True) # 设置索引
dt_index.to_sql('stock_index',  conn, if_exists='replace')

# 追加
codes.extend(indexs)

# 这里将中证500的数据导入
dt_zz500 = pd.read_csv(os.path.join(_file_dir_, 'zz500_stocks.csv'),encoding='utf-8')
dt_zz500.set_index('code',inplace=True) # 设置索引
dt_zz500.to_sql('stock_zz500',  conn, if_exists='replace')

# 深沪300的
dt_hs300 = pd.read_csv(os.path.join(_file_dir_, 'hs300_stocks.csv'),encoding='utf-8')
dt_hs300.set_index('code',inplace=True) # 设置索引
dt_hs300.to_sql('stock_hs500',  conn, if_exists='replace')

# 这里用到进度条
for i  in tqdm(range(len(codes))):
    _code_name = codes[i]
    # 第一个是删除
    _if_exists = 'append'
    csv_path = os.path.join(_file_dir_, "k线数据", f'{_code_name}.csv')
    # 这里删除所有数据
    if os.path.exists(csv_path):
        dt = pd.read_csv(csv_path,sep=',',parse_dates=['date'], encoding='utf-8') # 读取
        dt.set_index(['code', 'date'],inplace=True) # 设置索引,这里是多级索引
        dt.to_sql('stock_details', conn, if_exists=_if_exists) # 导入到数据库

# 最后关闭数据库
conn.close()