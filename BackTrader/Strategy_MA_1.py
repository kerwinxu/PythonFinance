#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-12-16 21:49:03
# File Name: sample1.py

import backtrader as bt
import CerebroBase
import StrategyBase

# Create a Stratey
# 这个是均线系统，我大选系统如下：
# 当五日均线突破10日均线的时候，10%仓位
# 当MACD出现突破的时候，10%仓位。


class Strategy_MA(StrategyBase.StrategyBase):

    params = (('ma1', 5), ('ma2', 10), ('ma3', 20))

    def __init__(self):
        # 添加多条均线
        self.sma1 = bt.talib.SMA(self.data, timeperiod=self.params.ma1)
        self.sma2 = bt.talib.SMA(self.data, timeperiod=self.params.ma2)
        self.sma3 = bt.talib.SMA(self.data, timeperiod=self.params.ma3)
        self.order = None

    def next(self):
        # size2 = int(value/open_price*0.25)
        # 我这里打算做几条判断，
        # 当5日均线大于10日均线的时候就买入，
        #   如果10日均线还大于20日均线，就加仓
        # 当5日均线少于10日均线的时候就卖出，
        #   如果10日均线还小于20日均线就加仓卖出
        if(self.sma1[0] > self.sma2[0]):
            # 首先判断是否有卖单子，如果有，就平仓。
            if(self.sma2[0] > self.sma3[0]):
                self.order = self.order_target_percent(target=0.20)
            else:
                self.order = self.order_target_percent(target=0.10)

        if(self.sma1[0] < self.sma2[0]):
            if(self.sma2[0] < self.sma3[0]):
                self.order = self.order_target_percent(target=-0.20)
            else:
                self.order =  self.order_target_percent(target=-0.10)


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = CerebroBase.CerebroAGTD()
    # Add a strategy
    cerebro.addstrategy(Strategy_MA)
    # Set our desired cash start
    cerebro.set_cash(200000.0)
    cerebro.show_analyzer(cerebro.run())
    cerebro.show_plot()
