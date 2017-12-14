#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-12-11 20:46:43
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

    params= (
        ('up_slope', 1.001),
        ('down_slope', 0.097)
    )

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # 添加自适应均线
        self.kama = bt.talib.KAMA(self.data)
        # To keep track of pending orders
        self.order = None

    def next(self):
        # 首先判断是否有订单
        # 如果没有订单，
        #   如果上涨到一定的斜率，就买单开仓
        #   如果下跌到一定的斜率，就卖单开仓
        # 如果有订单
        #   判断是加仓还是平仓
        #       先判断是买单还是卖单吧
        #           如果是买单：
        #               跌倒一定的速率就平仓
        #               根据海龟交易，加仓

        # 斜率
        _slope = self.kama[0] / self.kama[-1]
        #  算出可以购买的数量
        _kally_ratio = self.get_kally_ratio()
        _size = 1
        if not self.position:
            # 如果没有订单。
            if(_slope > self.params.up_slope):
                # 这里就是买单开仓了，
                self.order = self.buy()
            elif(_slope < self.params.down_slope):
                pass
                # self.order = self.sell()
        elif self.position.size > 0:
            # 到这里往往表示有订单了。
            if(_slope < self.params.up_slope):
                self.order = self.close()
        elif self.position.size < 0:
            if(_slope > self.params.down_slope):
                self.order = self.close()


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = CerebroBase.CerebroAGTD()
    # Add a strategy
    cerebro.addstrategy(Strategy_KAMA)

    # Set our desired cash start
    cerebro.set_cash(2000.0)

    cerebro.show_analyzer(cerebro.run())

    cerebro.show_plot()
