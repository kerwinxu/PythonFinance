#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-09-30 23:20:09
# File Name: sample1.py

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
# import os.path  # To manage paths
# import sys  # To find out the script name (in argv[0])
# import pandas as pd
# from WindPy import w
# Import the backtrader platform
import backtrader as bt
import sys
sys.path.append("../FinanceDataSource")
import FinanceDataSource


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
                self.log('BUY EXECUTED, %d, %.2f' %
                         (order.executed.size, order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED, %d, %.2f' %
                         (order.executed.size, order.executed.price))

            self.bar_executed = len(self)

        # Write down: no pending order
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # 我暂时的判断是当自适应均线拐角向上的时候，买入
        if self.kama[0] > self.kama[-1] and self.kama[-2] > self.kama[-1]:
            self.order = self.buy()
            pass
            # 只是买入1/10的钱
        elif self.kama[0] < self.kama[-1] and self.kama[-2] < self.kama[-1]:
            # 这里就是卖掉了
            self.order = self.sell()
            pass

        # Check if we are in the market
        if not self.position:
            pass
            # 如果没有订单。
        else:
            # 到这里往往表示有订单了。
            pass


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(Strategy_KAMA)

    # Create a Data Feed
    # 本地数据，笔者用Wind获取的东风汽车数据以csv形式存储在本地。
    # parase_dates = True是为了读取csv为dataframe的时候能够自动识别datetime格式的字符串，big作为index
    # 注意，这里最后的pandas要符合backtrader的要求的格式
    dataframe = FinanceDataSource.get_data(
        FinanceDataSource.str_tonghuashun, FinanceDataSource.tonghuashun_AGTD)
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

    # Set our desired cash start
    cerebro.broker.setcash(50000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Plot the result
    cerebro.plot()
