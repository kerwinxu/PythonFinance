# 这里是用akshare来做的，用新浪的数据吧
import pandas as pd
import os
import sqlite3


_file_dir_ = os.path.split(os.path.realpath(__file__))[0]

DB_FILE_NAME = 'sina_data.db'  # 数据库的文件,这个是新浪财经的数据
DB_FILE = os.path.join(_file_dir_, DB_FILE_NAME)

def runSql(sql:str):
    # 执行一个sql
    conn = sqlite3.connect(DB_FILE)
    dt = pd.read_sql(sql, conn)
    conn.close()
    return dt

def get_codes():
    # 取得所有的股票名称
    sql = f'select DISTINCT 代码 from codeNames;'
    return runSql(sql).loc[:,'代码'].tolist()

def getData(code, start_date=None, end_date=None):
    sql = f'select * from stock_daily where code="{code}" '
    if start_date is not None:
        sql += f' and date >= "{start_date}" '
    if end_date is not None:
        sql += f' and date <= "{end_date}"'
    sql += ' order by date'
    dt = runSql(sql)
    dt['Date'] = pd.to_datetime(dt['Date'], format=f'%Y-%m-%d %H:%M:%S')
    return dt

def get_code_last_date(code:str):
    # 取得这个股票最后的时间
    sql = f'select max(date) from stock_daily where code =  {code};'
    dt = runSql(sql)
    if len(dt) > 0:
        return dt.iloc[0,0]
    else:
        return None


if __name__ == '__main__':
    # 这里是作为文件运行的，下边主要是测试运行情况的
    # codes = get_codes()
    # print(f'现有股票数量:{len(codes)}, {codes}')
    # # 请注意，这里查询日期得是如下的格式。
    # datas = getData('000001', '2026-04-10', '2026-04-19')
    # print(datas.head())
    last_date = get_code_last_date('bj920000')
    print(last_date)