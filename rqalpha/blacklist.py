#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-02-07 21:49:23
"""@File Name: blacklist.py
@Author:  kerwin.cn@gmail.com
@Created Time:2018-02-05 16:44:07
@Last Change: 2018-02-05 16:44:07
@Description : 这个文件只是取得一堆黑名单的数据的。
这个黑名单有点未来函数的意思，毕竟谁知道哪个股票未来上黑名单。
这个最大的作用就是，上了黑名单的股票，未来不参与。
"""
import pandas as pd
import datetime
import talib
import sys
import os
sys.path.append(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        "../FinanceDataSource"))
sys.path.append("../FinanceDataSource")

from FinanceDataSource import get_cn_stock_basics
from FinanceDataSource import get_cn_finance_data
from FinanceDataSource import str_cn_report
from FinanceDataSource import get_quarter_pre
from FinanceDataSource import get_cn_last_finance_data
from FinanceDataSource import get_cn_last_finance_data_2


_lst_blacklist_area = ['黑龙江', '吉林', '辽宁']

_lst_blacklist_code = [
    '002069',   # 獐子岛
    '300104',   # 乐视
]


def remove_blacklist(lst):
    """
        Description : 这个函数的作用很简单，只是除去黑名单中的股票。
        Arg :
        Returns :
        Raises	 :
    """
    # 筛选掉黑名单地区的
    _lst = blacklist_area(lst)
    # 筛选掉黑名单股票
    _lst = [x for x in _lst if x not in [_lst_blacklist_code]]
    # 筛选掉ST股票
    _lst = remove_st_stock(_lst)
    # 筛选掉新的股票。
    _lst = remove_n_stock(_lst)
    return _lst


def remove_roe_lt(lst, _datetime=None, n=0):
    """
        Description : 筛选掉净资产收益率少于一定数量的股票。
            这个会根据某季度前面的最后4个季度的报表平均。
        Arg : 
            @lst : 要筛选的股票
            @year : 年份
            @quarter : 季度
            @n   : 净资产收益率。 
        Returns :
        Raises	 :
    """
    # 首先取得所有股票的相关信息
    _df = get_cn_last_finance_data_2(str_cn_report, lst, _datetime)
    _group = pd.DataFrame(_df.groupby('code').roe.mean())
    return list(_group[_group['roe'] > n].index)

    # 净资产收益率在tushare的业绩报告主表中。
    return [x for x in lst if (get_cn_last_finance_data(
        str_cn_report,
        x,
        _datetime, 4
    )['roe'].mean() > n)]


def if_row_lt(code, dt, n):
    # 净资产收益率在tushare的业绩报告主表中。
    if dt is None:
        dt = datetime.datetime.now()
    year, quarter = get_quarter_pre(dt)
    _df = get_cn_last_finance_data(str_cn_report, code, dt, 4)

    pass


def get_roe_mean(code, _datetime, n=4):
    """
        Description : 取得某个股票最近几次报表的roe平均值。
        Arg :
        Returns :
        Raises	 :
    """
    pass


def remove_st_stock(lst):
    """
        Description : 除去ST股票，我不想担风险。
        Arg :
        Returns :
        Raises	 :
    """
    return [x for x in lst if (
        get_cn_stock_basics(x) is not None and
        "ST" not in str(get_cn_stock_basics(x)['name']))]
    pass


def get_area(code):
    """
        Description : 输入股票ID，返回股票地区。
        Arg :
        Returns :
        Raises	 :
    """
    _basics = get_cn_stock_basics(code)
    if _basics is None:
        return None
    return _basics['area']
    pass


def blacklist_area(lst):
    """
        Description : 就是这几个地区的股票不要。
        Arg :
        Returns :
        Raises	 :
    """
    return [x for x in lst if get_area(x) not in _lst_blacklist_area]
    pass


def remove_n_stock(lst):
    """
        Description : 带N的股票也去掉吧，这些是新股
        Arg :
        Returns :
        Raises	 :
    """
    return [x for x in lst if (
        get_cn_stock_basics(x) is not None and
        "N" not in str(get_cn_stock_basics(x)['name']))]
    pass


if __name__ == '__main__':
    # print(get_area('000001'))
    print(remove_blacklist(
        ['000001', '002069', '000686', '002207', '300287', '000982']))
    print(remove_roe_lt(
        ['000001', '002069', '000686', '002207', '300287', '000982'], datetime.datetime.strptime("2017-07", "%Y-%m"), 0))
