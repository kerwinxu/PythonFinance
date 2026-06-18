from tqdm import tqdm
import os
import sqlite3
import pandas as pd

_file_dir_ = os.path.split(os.path.realpath(__file__))[0] # 本文件的目录
DB_FILE_NAME = 'data.db'  # 数据库的文件
DB_FILE = os.path.join(_file_dir_, DB_FILE_NAME)
# 这里先删除这个数据库
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

# 数据库部分
# 连接到 SQLite 数据库（如果不存在会自动创建）
conn = sqlite3.connect(DB_FILE)

# 遍历文件夹
new_data_dir = os.path.join(_file_dir_, './最新数据')
for file_path in os.listdir(new_data_dir):
    file_full_path = os.path.join(new_data_dir, file_path)
    dt = pd.read_csv(file_full_path
                    ,names=['code','index','date','open','high','low','close','money','volume']  # 自定义列名
                    ,parse_dates=['date']  # 指定日期列
                    ,header=0
                    ,index_col=['code', 'date'] # 设置索引
    )
    # 然后导出到数据库
    dt.to_sql(
        name='stocks'
        ,con=conn
        ,if_exists='append'
        ,chunksize=1000
    )


conn.close()