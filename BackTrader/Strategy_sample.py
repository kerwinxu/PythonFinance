#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-11-10 20:59:33
# Last Change:  2017-11-22 21:10:19
# File Name: Strategy_sample.py
# 这个文件只是作为策略编写的例子文件

# 首先导入这3个
# 因为还需要这个回测交易系统的很多指标，所以导入这个
import backtrader as bt
# 我做的大脑的基类，运行策略用
import CerebroBase
# 我做的策略的基类
import StrategyBase


class Strategy_sample(StrategyBase.StrategyBase):
    params = ()

    def __init__(self):
        """这个策略的构造器"""
        # 这里仅仅是初始化一个均线
        self.sma1 = bt.talib.SMA(self.data, timeperiod=self.params.ma1)

    def next(self):
        """
        这个策略的策略方法
        我认为，主要分如下几点：
            开仓 ：
                什么时候开仓
                开仓多少点
            加仓 ：
                什么时候加仓
                加仓多少点
            减仓 ：
                什么时候减仓
                减仓多少点
            平仓 ：
                什么时候平仓
        关于资金管理，大体如下:
            海龟交易 ： 海龟交易赢在资金管理，重要的是每次损失不超过1%
                是根据真实波幅ATR来计算可能的亏损，再计算需要投入的手数
            凯莉法则 ： 假设 p = 获胜的概率，q = 失败的概率，b = 赔率
                那么需要投入的资金为f = (bp - q) / b
                其中(bp - q) 可以理解为期望的盈利
                    如果这个为正，那么表示可以投入，
                    如果这个为负，表示不可以投入。

        """
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        pass

if __name__ == '__main__':
    #  测试策略在这里
    # Create a cerebro entity
    cerebro = CerebroBase.CerebroAGUSDO()
    # Add a strategy
    cerebro.addstrategy(Strategy_sample)
    # Set our desired cash start
    cerebro.set_cash(10000.0)
    #  run
    results = cerebro.run()
    # 显示分析师的结果
    cerebro.show_analyzer(results)
    # 用图表显示结果
    cerebro.show_plot()
