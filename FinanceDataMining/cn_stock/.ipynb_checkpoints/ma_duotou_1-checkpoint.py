
# coding: utf-8
# Last Change:  2018-01-30 19:13:39

# # 查看A股均线多头的情况

# ## 首先导入相关的库

# In[8]:


import sys
import os
sys.path.append(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        "../../FinanceDataSource"))
sys.path.append("../../FinanceDataSource")
import FinanceDataSource
import tushare as ts
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns  # 要注意的是一旦导入了seaborn，matplotlib的默认作图风格就会被覆盖成seaborn的格式
import pandas as pd
import numpy as np
from pandas import DataFrame
from FinanceDataSource import get_cn_stocks
from FinanceDataSource import get_data
from FinanceDataSource import str_cn_stock
from FinanceDataSource import get_cn_bars_all
import talib


class Ma_duotou():
    """
    这个类仅仅是保存多头信息的。我打算保存如下信息
    Attributes	:
        @book_id : 股票id
        @DateFrame : 将股票这几天的信息全部切片保存起来。方便以后运算。
    functions	:

    """

    def __init__(self, book_id, df):
        """
            Description :
            Arg :
            Returns :
            Raises	 :
        """
        self.book_id = book_id
        self.df_duotou = df
    pass


def get_ma_duotou_indicator(book_id, lst_ma):
    """
        Description : 将一个股票的均线多头用逻辑数组标记出来，并保存起来。
        Arg :
        Returns :
        Raises	 :
    """
    _close = get_cn_bars_all(book_id, fields='close')
    # 将所有的均线保存在这个数组中。
    _lst_ma = []
    for _ma in lst_ma:
        _lst_ma.append(talib.SMA(_close, _ma))
    _ma_0 = talib.SMA(_close, lst_ma[0])
    _ma_1 = talib.SMA(_close, lst_ma[1])
    _ma_2 = talib.SMA(_close, lst_ma[2])
    _ma_3 = talib.SMA(_close, lst_ma[3])

    _bool_up = list(
        map(lambda a, b, c, d:
            a > b and b > c and c > d,
            _ma_0, _ma_1, _ma_2, _ma_3))

    return _bool_up


def get_lst_ma_duotou(book_id, ma_duotou_indicator):
    """
        Description : 这个是从均线多头的逻辑数组中切片出连续多头的。
        Arg :
        Returns :
        Raises	 :
    """
    _data = get_cn_bars_all(book_id)     # 取得这个股票的k线
    _i = 0                                  # 遍历
    _lst_duotou = []                        # 保存所有的多头
    _count = len(ma_duotou_indicator)
    while _i < _count:    # 遍历
        if ma_duotou_indicator[_i]:         # 如果找到多头均线的起始点
            _start = _i                     # 保存一开始的下表
            while _i < _count and ma_duotou_indicator[_i]:  # 看看一共连续多少。
                _i = _i + 1
            # 创建一个类来保存这些信息吧
            # 保存的信息只是2点，一个就是股票id
            # 另外一个就是K线数据，用切片的来的。
            _cls_ma_duotou = Ma_duotou(book_id, _data[_start:_i])
            _lst_duotou.append(_cls_ma_duotou)
        _i = _i + 1     # 递增。
    return _lst_duotou


def get_all_lst_ma_duotou(lst_ma):
    """
        Description : 取得所有股票的多头数据，可以用其他程序进行分析的。
        Arg :
        Returns :
        Raises	 :
    """
    # 要记录所有多头信息的里列表
    _lst_duotou = []
    # 取得所有的股票
    _all_cn_stock = get_cn_stocks()

    # 遍历所有的股票, 先找出所有的多头趋势来。
    for _book_id in _all_cn_stock:
        _bool_up = get_ma_duotou_indicator(_book_id, lst_ma)
        _lst_duotou.extend(get_lst_ma_duotou(_book_id, _bool_up))
    return _lst_duotou


if __name__ == "__main__":
    _lst_ma_duotou = get_all_lst_ma_duotou([5, 10, 20, 60])
    print(len(_lst_ma_duotou))
    pass
