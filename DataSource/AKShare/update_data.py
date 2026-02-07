# 用来创建数据库
import pandas as pd
import os
import sqlite3
import akshare as ak
from tqdm import tqdm
import datetime
import time
import random

_file_dir_ = os.path.split(os.path.realpath(__file__))[0] # 本文件的目录
DB_FILE_NAME = 'data.db'  # 数据库的文件
DB_FILE = os.path.join(_file_dir_, DB_FILE_NAME)
START_DATE = '20200101'
# 获取当前时间
now = datetime.datetime.now()
END_DATE = now.strftime(f'%Y%m%d')


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


# 这里首先取得所有的股票列表
stock_info_a_code_name_df = ak.stock_info_a_code_name()
# 然后先导入到数据库重
stock_info_a_code_name_df.to_sql('codeNames',conn, if_exists='replace', index=False)

# 然后这里遍历
codes = list(stock_info_a_code_name_df['code'])
for i  in tqdm(range(len(codes))):
    code = codes[i] # 取得股票编码
    # 然后取得最后的时间
    start_date = START_DATE  # 默认是这个时间
    end_date = END_DATE      # 结束日期
    time.sleep(random.uniform(5, 10)) # 随机延迟3-5秒
    # ! 请注意，这个接口不行啊，连接一次后就异常
    # 取得数据
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="hfq")
    # 然后保存数据
    stock_zh_a_hist_df.to_sql(code,conn, if_exists='append', index=False)
    

# 最后关闭
conn.close()