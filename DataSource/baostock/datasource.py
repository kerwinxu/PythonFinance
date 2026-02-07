# 这个是作为数据源的脚本
import pandas as pd
import os
import sqlite3

_file_path_ = os.path.split(os.path.realpath(__file__))[0]

DB_FILE_NAME = 'data.db'  # 数据库的文件
DB_FILE = os.path.join(_file_path_, DB_FILE_NAME)

# 数据库部分


def get_data(code):
    """获得数据

    Args:
        code (_type_): _description_

    Returns:
        _type_: _description_
    """
    csv_path = os.path.join(_file_path_, "k线数据", f'{code}.csv')
    # 这里要判断是否有这个数据
    if os.path.exists(csv_path):
        dt = pd.read_csv(csv_path,sep=',',parse_dates=['date'], index_col=0)
        return dt
    else:
        return None

def get_codes():
    """获得所有股票的数据

    Returns:
        _type_: _description_
    """
    csv_path = os.path.join(_file_path_, "stock_industry.csv")
    dt = pd.read_csv(csv_path, sep=',',encoding='utf-8')
    return list(dt['code'])

def get_zz500_codes():
    """
        获得中正500股票的代码
    Returns:
        _type_: _description_
    """
    csv_path = os.path.join(_file_path_, "zz500_stocks.csv")
    dt = pd.read_csv(csv_path, sep=',',encoding='utf-8')
    return list(dt['code'])

def get_indexs():
    """_summary_
        获得所有的指数
    Returns:
        _type_: _description_
    """
    csv_path = os.path.join(_file_path_, "zz500_stocks.csv")
    dt = pd.read_csv(csv_path, sep=',',encoding='utf-8')
    return list(dt['code'])


def getData(code, start_date=None, end_date=None):
    # 搜索指定股票，可以指定开始结束日期
    # 连接到 SQLite 数据库（如果不存在会自动创建）
    conn = sqlite3.connect(DB_FILE)
    sql = f'select * from stock_details where code = "{code}" '
    if start_date is not None:
        sql += f' and date >= "{start_date}" '
    if end_date is not None:
        sql += f' and date <= "{end_date}"'
    sql += ' order by date'
    dt =  pd.read_sql(sql, conn, parse_dates='date', index_col='date')
    conn.close()
    return dt

def runSql(sql:str):
    # 执行一个sql
    conn = sqlite3.connect(DB_FILE)
    dt = pd.read_sql(sql, conn)
    conn.close()
    return dt

def getStockIndustry():
    # 取得所有的A股
    return runSql('select * from stock_industry')

def getStockIndex():
    return runSql('select * from stock_index')

def getZz500():
    # 取得中证500成分股
    return runSql('select * from zz500_stocks')