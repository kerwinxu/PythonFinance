#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2018-01-15 21:20:11
# File Name: sample1.py

# import os.path  # To manage paths
# import sys  # To find out the script name (in argv[0])
# import pandas as pd
# from WindPy import w
# Import the backtrader platform
import backtrader as bt
import CerebroBase
import StrategyBase
# Create a Stratey
# 这个是自适应均线交易系统


class Strategy_KAMA(StrategyBase.StrategyBase):

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # 添加自适应均线
        self.kama = bt.talib.KAMA(self.data)
        # To keep track of pending orders
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one

        # 我暂时的判断是当自适应均线拐角向上的时候，买入
        if self.kama[0] > self.kama[-1] and self.kama[-2] > self.kama[-1]:
            self.order = self.buy()
            pass
        elif self.kama[0] < self.kama[-1] and self.kama[-2] < self.kama[-1]:
            # 这里就是卖掉了
            self.order = self.close()
            pass

        # Check if we are in the market
        if not self.position:
            pass
            # 如果没有订单。
        else:
            # 到这里往往表示有订单了。
            pass
        print(1/0)


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = CerebroBase.CerebroAUTD()
    # Add a strategy
    cerebro.addstrategy(Strategy_KAMA)

    # Set our desired cash start
    cerebro.set_cash(5000.0)

    cerebro.show_analyzer(cerebro.run())

    cerebro.show_plot()
