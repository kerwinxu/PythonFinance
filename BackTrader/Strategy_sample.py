#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-11-10 20:59:33
# Last Change:  2017-11-10 21:30:46
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
        """这个策略的策略方法"""
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
    cerebro.set_cash(100000.0)
    #  run
    cerebro.run()
    # 显示分析师的结果
    cerebro.show_analyzer()
    # 用图表显示结果
    cerebro.show_plot()
