#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-12-16 22:30:33
# File Name: sample1.py
import backtrader as bt
import CerebroBase
import StrategyBase


# Create a Stratey
# 这个MACD系统
class Strategy_MACD(StrategyBase.StrategyBase):

    params = (('fastperiod', 12),
              ('slowperiod', 26),
              ('signalperiod', 9),
              ('ma1', 10),
              )

    def __init__(self):
        # 这个就是那个柱状
        self.macdhisto = bt.indicators.MACDHisto(self.data)
        self.sma1 = bt.talib.SMA(self.data, timeperiod=self.params.ma1)
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        size1 = self.get_right_sizing()
        _close = self.data_close[0]
        _sma1 = self.sma1[0]

        # if self.position.size > 0:
            # # 有买单，判断止损是小于均线
            # if _close < _stop_price:
                # self.order = self.close()
            # pass
        # elif self.position.size < 0:
            # # 有卖单，判断止损是大于均线
            # if _close > _stop_price:
                # self.order = self.close()
            # pass
        # 这里判断是否下单
        if(self.macdhisto[0] > 0
           and self.macdhisto[-1] < 0
           and _close > _sma1):
            self.order = self.buy(size=size1)
        if(self.macdhisto[0] < 0
           and self.macdhisto[-1] > 0
           and _close < _sma1):
            self.order = self.sell(size=size1)


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = CerebroBase.CerebroAGTD()
    # Add a strategy
    cerebro.addstrategy(Strategy_MACD)
    # Set our desired cash start
    cerebro.set_cash(5000.0)
    cerebro.show_analyzer(cerebro.run())
    cerebro.show_plot()
