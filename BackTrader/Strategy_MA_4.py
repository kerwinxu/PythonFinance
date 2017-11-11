#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-11-10 20:56:25
# File Name: sample1.py

import backtrader as bt
import CerebroBase
import StrategyBase

# Create a Stratey
# 这个是均线系统，我大选系统如下：
# 当五日均线突破10日均线的时候，通过胜率赔钱等判断仓位


class Strategy_MA(StrategyBase.StrategyBase):
    params = (
        ('ma1', 5),
        ('ma2', 20),
        ('ma3', 20)
    )

    def get_need_position(self):
        """根据凯莉公式计算需要的仓位"""
        try:
            # 首先取得TradeAnalyzer，这里有胜率，盈利金额，等等信息
            ta = self.analyzers.TradeAnalyzer.get_analysis()
            order_count = ta['total']['closed']
            won_count = ta['won']['total']
            won_average = ta['won']['pnl']['average']
            # lost_count = ta['lost']['total']
            lost_average = abs(ta['lost']['pnl']['average'])
            peilv = won_average / lost_average
            # kaili = (won_count / order_count * peilv - lost_count / order_count) / (peilv)
            p = won_count / order_count
            kaili = p - (1 - p) / peilv

            if(kaili > 0.5 or kaili < 0.05):
                return 0.10
            return kaili
        except Exception as err:
            self.log(err, isprint=True)
            return 0.10

    def __init__(self):
        # 添加多条均线
        self.sma1 = bt.talib.SMA(self.data, timeperiod=self.params.ma1)
        self.sma2 = bt.talib.SMA(self.data, timeperiod=self.params.ma2)
        self.sma3 = bt.talib.SMA(self.data, timeperiod=self.params.ma3)
        self.order = None

    def next(self):
        """
        我打算5日上穿10日均线的，开仓。
        """
        if(self.sma1[0] > self.sma2[0] and
           self.sma1[-1] < self.sma2[-1]):
            # 买单开仓啦
            pos_percent = self.get_need_position()
            self.order = self.order_target_percent(target=pos_percent)
            self.log("买单仓位：%s" % (pos_percent), isprint=True)
            pass
        elif(self.sma1[0] < self.sma2[0] and
             self.sma1[-1] > self.sma2[-1]):
            # 卖单开仓啦
            pos_percent = self.get_need_position()
            self.order = self.order_target_percent(target=0 - pos_percent)
            self.log("卖单仓位：%s" % (pos_percent), isprint=True)
        pass

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = CerebroBase.CerebroAGUSDO()
    # Add a strategy
    cerebro.addstrategy(Strategy_MA)
    # Set our desired cash start
    cerebro.set_cash(100000.0)
    cerebro.run()
