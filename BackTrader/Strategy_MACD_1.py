#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-11-14 22:03:36
# File Name: sample1.py
import backtrader as bt
import CerebroBase
import StrategyBase


# Create a Stratey
# 这个MACD系统
class Strategy_MACD(StrategyBase.StrategyBase):

    params = (('fastperiod', 12), ('slowperiod', 26), ('signalperiod', 9))

    def __init__(self):
        # 这个就是那个柱状
        self.macdhisto = bt.indicators.MACDHisto(self.data)
        self.order = None

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
        if(self.macdhisto[0] > 0
           and self.macdhisto[-1] < 0):
            self.buy(size=size1)

        if(self.macdhisto[0] < 0
           and self.macdhisto[-1] > 0):
            self.sell(size=size1)


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = CerebroBase.CerebroAGTD()
    # Add a strategy
    cerebro.addstrategy(Strategy_MACD)
    # Set our desired cash start
    cerebro.set_cash(5000.0)
    cerebro.run()
    cerebro.show_plot()
