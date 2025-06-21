#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-03 11:23:33
# Last Change:  2018-04-10 22:39:07
# File Name: init_data.py

"""
这个文件是用来初始化金融数据的，暂时是从quandl中取得数据
注意 ： 从这里边取得的伦敦金银是没有开盘价最高价最低价的。

"""
import quandl
from pandas_datareader import data as web
import time
import datetime
import pandas
import os
import chardet
import numpy as np
import tushare as ts

# 可以使用rqalpha的数据
import rqalpha_data
from rqalpha_data import get_bars_all as get_cn_bars_all
from rqalpha_data import get_bars as get_cn_bars
from rqalpha_data import get_bar as get_cn_bar
from rqalpha_data import history_bars as get_cn_history_bars
from rqalpha_data import is_trading_date as is_cn_trading_date
from rqalpha_data import get_all_instruments as get_cn_all_instruments
from rqalpha_data import is_st_stock as is_cn_st_stock
from rqalpha_data import instruments as get_cn_instruments

# 查看tushare的数据
# from tushare_data.tushare_data import get_all_cashflow_data as get_cn_all_cashflow_data
# from tushare_data.tushare_data import get_all_debtpaying_data as get_cn_all_debtpaying_data
# from tushare_data.tushare_data import get_all_finance_data as get_cn_all_finance_data
# from tushare_data.tushare_data import get_all_growth_data as get_cn_all_growth_data
# from tushare_data.tushare_data import get_all_operation_data as get_cn_all_operation_data
# from tushare_data.tushare_data import get_all_profit_data as get_cn_all_profit_data
# from tushare_data.tushare_data import get_all_report_data as get_cn_all_report_data
# from tushare_data.tushare_data import get_finance_data as get_cn_finance_data
# from tushare_data.tushare_data import get_stock_basics as get_cn_stock_basics
# from tushare_data.tushare_data import get_last_finance_data as get_cn_last_finance_data
# from tushare_data.tushare_data import get_last_finance_data_2 as get_cn_last_finance_data_2

# from tushare_data.tushare_data import str_cashflow as str_cn_cashflow
# from tushare_data.tushare_data import str_debtpaying as str_cn_debtpaying
# from tushare_data.tushare_data import str_growth as str_cn_growth
# from tushare_data.tushare_data import str_operation as str_cn_operation
# from tushare_data.tushare_data import str_profit as str_cn_profit
# from tushare_data.tushare_data import str_report as str_cn_report

from tushare_data.tushare_data_3 import session
from tushare_data.tushare_data_3 import session_close
from tushare_data.tushare_data_3 import stock_basics_table
from tushare_data.tushare_data_3 import stock_cashflow_data
from tushare_data.tushare_data_3 import stock_debtpaying_data
from tushare_data.tushare_data_3 import stock_growth_data
from tushare_data.tushare_data_3 import stock_operation_data
from tushare_data.tushare_data_3 import stock_operation_data
from tushare_data.tushare_data_3 import stock_profit_data
from tushare_data.tushare_data_3 import stock_report_data
from tushare_data.tushare_data_3 import get_fundamentals
from tushare_data.tushare_data_3 import func


# 这里只需要定义符号就可以了
# quandl的符号相关
str_quandl = "quandl"
quandl_lbma_gold = "LBMA/GOLD"
quandl_lbma_silver = "LBMA/SILVER"
quandl_fed_jrxwtfb_n_b = "FED/JRXWTFB_N_B"
download_quandl = [quandl_lbma_gold,
                   quandl_lbma_silver,
                   quandl_fed_jrxwtfb_n_b]

# pandas_datareader相关
str_pandas_datareader = "yahoo"
yahoo_gold = "GC=F"         # 雅虎财经上的黄金期货
yahoo_silver = "SI=F"       # 白银期货
yaoo_crude_oil = "CL=F"     # 原油期货
yahoo_s_p_500 = "^GSPC"     # 标普500
yahoo_dow_30 = "^DJI"       # 道琼斯
yahoo_nasdaq = "^IXIC"      # 纳斯达克

download_yahoo = [yahoo_gold,
                  yahoo_silver,
                  yaoo_crude_oil,
                  yahoo_s_p_500,
                  yahoo_dow_30,
                  yahoo_nasdaq]

# 从同花顺下载的数据
# 这个数据是手动下载的
str_tonghuashun = "同花顺"
tonghuashun_AGUSDO = "AGUSDO"   # 伦敦银
tonghuashun_AUUSDO = "AUUSDO"   # 伦敦金
tonghuashun_USDIND = "USDIND"   # 美元指数
tonghuashun_AGTD = "AGTD"       # 上海黄金交易所的白银TD
tonghuashun_AUTD = "AUTD"       # 上海黄金交易所的黄金TD

str_cn_stock = "CN_STOCK"   # 中国股市

# 规范k线名称
str_date = "Date"
str_open = 'Open'
str_close = 'Close'
str_high = 'High'
str_low = 'Low'

tonghuashun_dict_columns = {
    "时间": "Date",
    "开盘": "Open",
    "最高": "High",
    "最低": "Low",
    "收盘": "Close",
    "涨幅": "Increase",
    "振幅": "Swing",
    "总手": "Volume",
    "金额": "Amount",
    "换手%": "ChangedHand",
    "成交次数": "VolAmount",
    "未平仓合约": "OpenInterest",
}

cn_stock_dict_columns = {
    "date": "Date",
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "value": "Volume",
    "total_turnover": "Amount",
}


def get_csv_file_name(data_supplier, symbol, ext='csv'):
    """
    输入数据提供者和符号，取得CSV文件名的
    """
    # 因为符号中经常有非法字符，所以这里用字符串替换一下。
    code = symbol.replace("/", "_")
    csv_file_name = "".join(["data/", data_supplier, "_", code, ".", ext])
    this_file_path = os.path.abspath(__file__)          # 这个方式可以得到这个文件的绝对路径
    this_file_dir = os.path.dirname(this_file_path)     # 取得这个文件所在的目录
    # 这样就取得的是绝对路径
    return os.path.join(this_file_dir, csv_file_name)


def get_data(data_supplier, symbol):
    """取得数据，方便的取得数据的"""
    # 如果是同花顺，就调用同花顺的方法。
    if (data_supplier == str_tonghuashun):
        return get_tonghuashun_data(symbol)
    # 如果是中国股市，用rqalpha_data的吧。
    if(data_supplier == str_cn_stock):
        return get_cn_stock_data(symbol)
    return pandas.read_csv(get_csv_file_name(data_supplier, symbol), parse_dates=True, index_col="Date")


def get_cn_stock_data(symbol):
    """
        Description : 取得股票数据
        Arg :
        Returns :
        Raises	 :
    """
    _data = get_cn_bars_all(symbol,
                            dt=datetime.datetime.now(),
                            convert_to_dataframe=True)
    _data.rename(columns=cn_stock_dict_columns, inplace=True)
    return _data
    pass


def yahoo_download_data(stock_name):
    start = datetime.datetime(2000, 1, 1)
    end = datetime.date.today()
    data = web.DataReader(stock_name, "yahoo", start, end)
    print("下载 {0}，数据量：{1}".format(stock_name, len(data)))
    csv_file_name = get_csv_file_name(str_pandas_datareader, stock_name)
    data.to_csv(csv_file_name)


def quandl_download_data(stock_name):
    """
        从quandl下载金融数据的
        Args :
            stock_name : 金融品种
            csv_file_name : 要保存到的CSV文件
    """
    # 得有key啊
    quandl.ApiConfig.api_key = "TX__sAMFHm3ckYYyEHu7"
    # 默认下载的就是pandas
    data = quandl.get(stock_name)
    print("下载 {0}，数据量：{1}".format(stock_name, len(data)))
    csv_file_name = get_csv_file_name(str_quandl, stock_name)
    data.to_csv(csv_file_name)


def get_tonghuashun_data(symbol):
    """取得数据的, 因为同花顺的数据中有文件名中文, 间隔为制表符，且列名为中文，所以这里要单独处理"""
    # 因为有些列名是中文，所以这里用这种方式
    path = get_csv_file_name(str_tonghuashun, symbol, "xls")
    # 首先判断是什么编码
    rawdata = open(path, "rb").read()
    result = chardet.detect(rawdata)
    charenc = result['encoding']
    # 然后根据编码打开文件
    f = open(path, encoding=charenc)
    # 因为同花顺的日期格式有些不同，1994-09-12,一
    # 这里还得对时间进行转换，因为metalotlib不认这个时间格式啊。
    data = pandas.read_csv(f, sep='\t', parse_dates=["时间"], index_col="时间", date_parser=strftime, thousands=',', dtype={
        "开盘": np.float64,
        "最高": np.float64,
        "最低": np.float64,
        "收盘": np.float64
        # "总手":np.float64,
        # "金额":np.float64
    })
    # 然后修改日期格式
    data.rename(columns=tonghuashun_dict_columns, inplace=True)
    return data


def strftime(x):
    return datetime.datetime.strptime(str(x).split(',')[0], "%Y-%m-%d")


def init_data():
    for symbol in download_quandl:
        quandl_download_data(symbol)
    # 因为雅虎的不太稳定，所以加异常处理吧
    is_download_ok = False  # 是否下载了
    for symbol in download_yahoo:
        field_count = 0     # 失败次数
        is_download_ok = False
        while(is_download_ok is False and field_count < 5):     # 最多允许5次错误吧
            try:
                yahoo_download_data(symbol)
                is_download_ok = True
            except Exception as err:
                print(err)
                print("下载失败：" + symbol)
                field_count = field_count + 1
                print("失败次数：" + str(field_count))
                print("暂停3秒钟")
                time.sleep(3)


def get_cn_stocks():
    """
        Description : 取得中国所有可以测试交易的股票列表，去掉ST和刚开市90天的股票。
        Arg :
        Returns :
        Raises	 :
    """
    _all_cn_stock = list(get_cn_all_instruments('CS')['order_book_id'])
    return [_stock for _stock in _all_cn_stock if (not
                                                   is_cn_st_stock(_stock, 1) and
                                                   (datetime.datetime.now() - get_cn_instruments(_stock).listed_date).days > 90)]
    pass


def get_quarter(_datetime):
    """
        Description : 根据日期返回年份季度
        Arg :
        Returns : (年份, 季度)
        Raises	 :
    """
    if (not isinstance(_datetime, datetime.datetime)):
        return None
    str_month = _datetime.strftime('%m')
    str_year = _datetime.strftime("%Y")
    if str_month in ['01', '02', '03']:
        return (str_year, '1')
    elif str_month in ['04', '05', '06']:
        return (str_year, '2')
    elif str_month in ['07', '08', '09']:
        return (str_year, '3')
    elif str_month in ['10', '11', '12']:
        return (str_year, '4')


def get_quarter_pre(_datetime):
    """
        Description : 取得某日期的上一个月份季度。
        Arg :
        Returns :
        Raises	 :
    """
    year, quarter = get_quarter(_datetime)
    if year is None:
        return None
    if quarter == '1':
        # 上一年啦。
        return str(int(year) - 1), '4'
    else:
        return year, str(int(quarter) - 1)

    pass


if __name__ == "__main__":
    # init_data()
    # df = get_cn_bars('600469.XSHG', '2017-11-01', 5, fields=['datetime', 'open', 'close'])
    # print(df)
    # df = get_cn_bars_all('600469.XSHG', '2017-11-01' fields=['datetime', 'open', 'close'])
    # print(df)
    # print(get_data(str_cn_stock, '600469.XSHG'))
    # print(get_cn_all_instruments('CS'))
    # print(get_cn_instruments('600469.XSHG'))
    # print(get_data(str_tonghuashun, tonghuashun_AGTD))
    print(get_cn_stocks())
    pass
