#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-11-11 20:59:17
# File Name: sample1.py
# import datetime  # For datetime objects
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
        k = self.kama
        h = self.data_high
        l = self.data_low
        p_s = self.position.size

        # 我的判断是，当最低价也高过均线价格。且单子少于等于0，就买入一部分，且设置止损价格为均线价格
        # 这里是连续2天突破均线才下单。
        if l[0] > k[0] and l[-1] > k[-1] and p_s <= 0:
            self.order = self.order_target_percent(target=0.1)
            self.sell(
                price=self.kama[0],
                size=self.order.size,
                executed=bt.Order.Stop,
                transmit=False,
                parent=self.order)
        if h[0] < k[0] and h[-1] < k[-1] and p_s >= 0:
            self.order = self.order_target_percent(target=-0.1)
            self.buy(
                price=self.kama[0],
                size=self.order.size,
                executed=bt.Order.Stop,
                transmit=False,
                parent=self.order)


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = CerebroBase.CerebroAGUSDO()
    # Add a strategy
    cerebro.addstrategy(Strategy_KAMA)

    # Set our desired cash start
    cerebro.set_cash(100000.0)

    cerebro.run()

    cerebro.show_plot()
