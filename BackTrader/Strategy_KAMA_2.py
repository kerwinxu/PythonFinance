#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-10-03 16:36:18
# File Name: sample1.py

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# import datetime  # For datetime objects
# import os.path  # To manage paths
# import sys  # To find out the script name (in argv[0])
# import pandas as pd
# from WindPy import w
# Import the backtrader platform
import backtrader as bt
import sys
sys.path.append("../")
# from FinanceDataMining import init_data


# Create a Stratey
# 这个是自适应均线交易系统
class Strategy_KAMA(bt.Strategy):

    def log(self, txt, dt=None):
        ''''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # 添加自适应均线
        self.kama = bt.talib.KAMA(self.data)
        # To keep track of pending orders
        self.order = None

    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log('BUY EXECUTED, %d, %.2f' % (order.executed.size, order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED, %d, %.2f' % (order.executed.size, order.executed.price))

            self.bar_executed = len(self)

        # Write down: no pending order
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        k = self.kama
        h = self.data_high
        l = self.data_low
        p_s = self.position.size

        # 我的判断是，当最低价也高过均线价格。且单子少于等于0，就买入一部分，且设置止损价格为均线价格
        # 这里是连续2天突破均线才下单。
        if l[0] > k[0] and l[-1] > k[-1] and p_s <= 0:
            self.order = self.order_target_percent(target=0.1)
            self.sell(price=self.kama[0], size=self.order.size, executed=bt.Order.Stop, transmit=False, parent=self.order)
        if h[0] < k[0] and h[-1] < k[-1] and p_s >= 0:
            self.order = self.order_target_percent(target=-0.1)
            self.buy(price=self.kama[0], size=self.order.size, executed=bt.Order.Stop, transmit=False, parent=self.order)
"""
收益率不怎么样。
Final Portfolio Value: 101954.11
夏普比率: OrderedDict([('sharperatio', -0.3973477640025947)])
最大回撤: AutoOrderedDict([('len', 1567), ('drawdown', 8.149751729860053), ('moneydown', 9046.253799999657), ('max', AutoOrderedDict([('len', 1567), ('drawdown', 8.22337095022286), ('moneydown', 9127.97139999966)]))])
年化收益： OrderedDict([('rtot', 0.019352591731643536), ('ravg', 8.713458681514424e-06), ('rnorm', 0.0021982041035608565), ('rnorm100', 0.21982041035608565)])

"""
