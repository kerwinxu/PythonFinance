# 这个是作为数据源的脚本
import pandas as pd
import os
import sqlite3

_file_path_ = os.path.split(os.path.realpath(__file__))[0]

DB_FILE_NAME = 'data.db'  # 数据库的文件
DB_FILE = os.path.join(_file_path_, DB_FILE_NAME)

def runSql(sql:str):
    # 执行一个sql
    conn = sqlite3.connect(DB_FILE)
    dt = pd.read_sql(sql, conn)
    conn.close()
    return dt

def getData(code=None, start_date=None, end_date=None):
    '''取得股票数据，请注意日期格式是"2023-01-01"'''
    # 连接到 SQLite 数据库（如果不存在会自动创建）
    conn = sqlite3.connect(DB_FILE)
    lst_where = [] # where条件放在这里边
    sql = f'select * from stocks ' # 起始
    # 如下判断是否有where
    if code is not None:
        lst_where.append(f'code = "{code}"')
    if start_date is not None:
        lst_where.append(f' date >= "{start_date}" ')
    if end_date is not None:
        lst_where.append(f' date <= "{end_date}"')
    # 这里判断一下是否有where
    if len(lst_where)>0:
        sql += ' where ' + ' and '.join(lst_where)
    # 排序
    sql += ' order by code, date'
    dt =  pd.read_sql(sql, conn, parse_dates='date', index_col=['code', 'date'])
    conn.close()
    return dt


def getAStockCodes():
    # 取得A股股票列表
    dt = runSql('select DISTINCT  code from stocks')
    lst = dt['code'].tolist()
    return lst


if __name__ == '__main__':
    # 这里测试取得股票列表
    lst_codes = getAStockCodes()
    print('股票列表节选')
    print(lst_codes[:10])
    dt = getData(lst_codes[0], start_date='2023-01-01', end_date='2023-12-12')
    print(dt.head())
    pass