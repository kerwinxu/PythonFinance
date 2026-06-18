# 这个是作为数据源的脚本
import pandas as pd
import os
import sqlite3

_file_path_ = os.path.split(os.path.realpath(__file__))[0]

DB_FILE_NAME = '同花顺导入\\同花顺导入\\bin\\x86\\Debug\\sqlite.db'  # 数据库的文件
DB_FILE = os.path.join(_file_path_, DB_FILE_NAME)


def runSql(sql:str):
    # 执行一个sql
    conn = sqlite3.connect(DB_FILE)
    dt = pd.read_sql(sql, conn)
    conn.close()
    return dt

def get_codes():
    # 取得所有的股票名称
    sql = f'select DISTINCT code from D1BarFileModel;'
    return runSql(sql)

def getData(code, start_date=None, end_date=None):
    sql = f'select * from D1BarFileModel where code="{code}" '
    if start_date is not None:
        sql += f' and date >= "{start_date}" '
    if end_date is not None:
        sql += f' and date <= "{end_date}"'
    sql += ' order by date'
    return runSql(sql)


if __name__ == '__main__':
    # 这里是作为文件运行的，下边主要是测试运行情况的
    codes = get_codes()
    print(f'现有股票数量:{len(codes)}')
    # 请注意，这里查询日期得是如下的格式。
    datas = getData('000001', '2026-04-10', '2026-04-19')
    print(datas.head())