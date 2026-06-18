# 用来创建数据库
import pandas as pd
import os
import sqlite3
import akshare as ak
from tqdm import tqdm
import datetime
import time
import random
import datasource

_file_dir_ = os.path.split(os.path.realpath(__file__))[0] # 本文件的目录
DB_FILE_NAME = 'sina_data.db'  # 数据库的文件,这个是新浪财经的数据
DB_FILE = os.path.join(_file_dir_, DB_FILE_NAME)
START_DATE = '2010-01-01'
# 获取当前时间
now = datetime.datetime.now()
END_DATE = now.strftime(f'%Y-%m-%d')


print(f'数据库文件:{DB_FILE}')

# 连接到 SQLite 数据库（如果不存在会自动创建）
conn = sqlite3.connect(DB_FILE)


# 如下是sqlite的小操作
def check_table_exists(conn:sqlite3.Connection, table_name:str):
    # 判断表是否存在
    cursor = conn.cursor()
    # 查询是否存在
    query = 'select name  from sqlite_master where type="table" and name=?;'
    cursor.execute(query, (table_name,)) # 执行查询
    result = cursor.fetchone() # 取得数据
    return result is not None  # 根据是否取得数据来判断是否存在
    pass

def get_last_date(conn:sqlite3.Connection, code:str):
    # 取得最后的日期
    cursor = conn.cursor()
    query = f'select name  from sqlite_master where type="table" and name=?;'
    pass

def get_code_last_date(conn:sqlite3.Connection, code:str):
    # 取得这个股票最后的时间
    try:
        cursor = conn.cursor()
        # 查询是否存在
        query = 'select max(date) as max_date from stock_daily where code = ?;'
        cursor.execute(query, (code,)) # 执行查询
        result = cursor.fetchone() # 取得数据
        return result[0] # 根据是否取得数据来判断是否存在
    except:
        return None
    pass

# 这里首先取得所有的股票列表，这个是从新浪财经取得的代码列表
stock_info_a_code_name_df = ak.stock_zh_a_spot()
# 然后先导入到数据库重
stock_info_a_code_name_df.to_sql('codeNames',conn, if_exists='replace', index=False)

# 然后这里遍历
codes = stock_info_a_code_name_df['代码'].tolist()
for i  in tqdm(range(len(codes))):
    code = codes[i] # 取得股票编码
    # 然后取得最后的时间
    start_date = START_DATE  # 默认是这个时间
    end_date = END_DATE      # 结束日期
    time.sleep(random.uniform(3, 5)) # 随机延迟3-5秒
    # 取得这个代码的最后时间
    if check_table_exists(conn, 'stock_daily'):
        # 这里要判断一下是否存在这个表
        _last_date = get_code_last_date(conn, code)
        if _last_date is not None:
            start_date = _last_date
    # 这里需要将日期增加一天
    start_date = datetime.strptime(start_date, f"%Y-%m-%d")
    start_date += datetime.timedelta(days=1)
    start_date = start_date.strftime(f'%Y-%m-%d')
    # 取得数据，这个是从新浪财经取得的数据，这里用后复权，不用调整前面的。
    stock_zh_a_hist_df = ak.stock_zh_a_daily(
        symbol=code, 
        start_date=start_date.replace('-', ''), 
        end_date=end_date.replace('-', ''), 
        adjust="hfq")
    # 如果有数据，则进入下一步。
    if len(stock_zh_a_hist_df)>0:
        stock_zh_a_hist_df['code']=code
        stock_zh_a_hist_df.set_index(['date', 'code'], inplace=True)  # 设置两列为索引
        # 然后保存数据
        stock_zh_a_hist_df.to_sql('stock_daily',conn, if_exists='append', index=True)
    

# 最后关闭
conn.close()