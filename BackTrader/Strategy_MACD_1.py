#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-10-02 23:51:47
# File Name: sample1.py

# from __future__ import (absolute_import, division, print_function,
#                         unicode_literals)

# import datetime  # For datetime objects
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
# 这个MACD系统


class Strategy_MACD(bt.Strategy):

    params = (('fastperiod', 12), ('slowperiod', 26), ('signalperiod', 9))

    def log(self, txt, dt=None):
        ''''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 这个就是那个柱状
        self.macdhisto = bt.indicators.MACDHisto(self.data)
        self.order = None

    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, %d, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.size,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.opsize = order.executed.size
            else:  # Sell
                self.log(
                    'SELL EXECUTED, %d, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.size,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm))

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        # 先求还有多少钱吧, cash是get_cash, 如果是要资产是get_value()
        cash = self.broker.get_value()
        # value = self.broker.get_value()
        # 获得开盘价格，我是根据开盘价格来交易的。
        open_price = self.data_open[0]

        size1 = int(cash / open_price * 0.1)
        # size2 = int(value/open_price*0.25)
        # 当5日均线上穿10日均线的时候，买入
        if(self.macdhisto[0] > 0
           and self.macdhisto[-1] < 0):
            self.buy(size=size1)

        if(self.macdhisto[0] < 0
           and self.macdhisto[-1] > 0):
            self.sell(size=size1)


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(Strategy_MACD)

    # 设置佣金杠杆
    # 上海黄金交易所手续费为万分之8，白银的递延费为万分之1.5， * 362 = 0.05475，这里不考虑杠杆。
    cerebro.broker.setcommission(commission=0.0008, interest=0.05475)

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

    # 每股固定10个
    # cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

    # 加入分析师
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')

    # Set our desired cash start
    cerebro.broker.setcash(50000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    results = cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Plot the result
    # cerebro.plot()

    # 显示分析师结果
    strat = results[0]
    print('夏普比率:', strat.analyzers.SharpeRatio.get_analysis())
    print('最大回撤:', strat.analyzers.DW.get_analysis())
