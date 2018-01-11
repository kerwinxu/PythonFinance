#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-01-10 21:53:32
"""@File Name: example.py
@Author:  kerwin.cn@gmail.com
@Created Time:2018-01-10 21:18:00
@Last Change: 2018-01-10 21:18:00
@Description :
"""
from rqalpha.api import add_indicator
from rqalpha.api import all_instruments
from rqalpha.api import get_bars_all
from rqalpha.api import history_bars

import talib

def init(self):
    """
        Description : 程序初始化
        Arg :
        Returns :
        Raises	 :
    """
    pass

def before_trading(self):
    """
        Description : 每天交易策略开始前被调用。
        Arg :
        Returns :
        Raises	 :
    """
    pass

def handle_bar(self, bar_dict):
    """
        Description : 选择的证券的数据更新将会触发此段逻辑
        Arg :
        Returns :
        Raises	 :
    """
    pass

def after_trading(self):
    """
        Description : 每天交易结束后调用。
        Arg :
        Returns :
        Raises	 :
    """
    pass
