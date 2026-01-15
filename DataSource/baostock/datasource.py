# 这个是作为数据源的脚本
import pandas as pd
import os
_file_path_ = os.path.split(os.path.realpath(__file__))[0]

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