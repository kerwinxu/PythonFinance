#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-01-17 21:14:19
"""@File Name: AUTD_up_down.py
@Author:  kerwin.cn@gmail.com
@Created Time:2017-12-28 20:58:42
@Last Change: 2017-12-28 20:58:42
@Description :  这个是取得zip转向数据的。
"""

import sys
import os
sys.path.append(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        "../../FinanceDataSource"))
sys.path.append("../../FinanceDataSource")

from FinanceDataSource import is_cn_st_stock
from FinanceDataSource import get_cn_bars_all
from FinanceDataSource import get_cn_all_instruments
from FinanceDataSource import get_data
from FinanceDataSource import str_cn_stock
from FinanceDataSource import get_cn_stocks

import datetime
import numpy as np
import shelve
import pandas as pd


def get_zip(N, M, N2):
    """
        Description : 取得A股所有股票的图片N日新高，且大于最低点M%后N2日后最高最低百分比。
        Arg :
            @N： 前面N日
            @M： M%
            @N2 ： 后边N2日
        Returns :
        Raises	 :
    """
    # 删除ST股票, 不对ST股票做回测。
    # 上市90天的股票不做回测，因为前几天都是疯涨。然后暴跌。
    _all_cn_stock = get_cn_stocks()

    _date = []
    _stock_name = []
    _up = []
    _down = []
    # 遍历所有股票
    for _book_id in _all_cn_stock:
        try:
            # 取得这个股票的所有数据。
            _data = get_data(str_cn_stock, _book_id)
            _close = _data["Close"]

            # 然后遍历这个收盘价，前面的减去相应天数，后边的也减去相应天数。
            for _i in range(N, len(_close)-N2):
                _current = _close[_i]
                _before = _close[_i-N:_i]
                _before_min = min(_before)
                _before_max = max(_before)
                # 判断是否突破
                if (
                        _current > _before_min * (100+M)/100
                        and _current == _before_max):
                    _after = _close[_i+1:_i+N2]
                    _after = [j for j in _after if j != 0]
                    _after_max = max(_after)
                    _after_min = min(_after)
                    _up.append((_after_max - _current)/_current*100)
                    _down.append((_after_min - _current)/_current*100)
                    _stock_name.append(_book_id)
                    _date.append(_data.index[_i])
        except:
            pass
    _DateFrame = pd.DataFrame(
            data={
                "Stock_ID": _stock_name,
                "Up": _up,
                "Down": _down
                },
            index=_date)
    return _DateFrame


if __name__ == "__main__":
    _df = get_zip(20, 10, 20)
    _csv_file = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)),
            "zip_cn_stock.csv")
    _df.to_csv(_csv_file)
