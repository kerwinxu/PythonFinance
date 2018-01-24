#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-01-13 16:29:49
"""@File Name: ADX_1.py
@Author:  kerwin.cn@gmail.com
@Created Time:2018-01-13 15:21:48
@Last Change: 2018-01-13 15:21:48
@Description :
"""
import sys
import os
sys.path.append(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        "../../FinanceDataSource"))
sys.path.append("../../FinanceDataSource")
import FinanceDataSource
sys.path.append(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        "../../CandlestickOhlc"))
sys.path.append("../../CandlestickOhlc")
from CandlestickOhlc import candlestickohlc

import datetime
import talib


_book_id = "600469.XSHG"

_data = FinanceDataSource.get_data(FinanceDataSource.str_cn_stock, _book_id)

_data["ADX"] = talib.ADX(_data["High"].as_matrix(),
                         _data["Low"].as_matrix(),
                         _data['Close'].as_matrix())

candlestickohlc(_data,otherseries=["ADX"])
