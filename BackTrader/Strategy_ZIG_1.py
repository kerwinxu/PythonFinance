#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-11-10 20:59:33
# Last Change:  2017-11-22 20:12:14
# File Name: Strategy_sample.py
# 这个文件只是作为策略编写的例子文件

# 首先导入这3个
# 因为还需要这个回测交易系统的很多指标，所以导入这个
import backtrader as bt
# 我做的大脑的基类，运行策略用
import CerebroBase
# 我做的策略的基类
import StrategyBase


class Strategy_ZIG(StrategyBase.StrategyBase):
    """
    这个是根据zig转向设计的策略系统
    属性 :

    实例属性:
        isUp : 表示这个是上涨
        extremum : 表示极值，最大值或者最小值
    方法 :
        next : 读取每个k线后执行的回调函数

    这个交易系统没有编写，理由是：
    这个是未来函数，放在测试中是有些作弊，
    毕竟谁知道当天是最高点或者最低点，
    而如果事后判断，往往行情已经过半了，
    接下来的风险太大。
    """

    params = ()

    def __init__(self):
        """这个策略的构造器"""
        # 这里仅仅是初始化一个均线
        self.isUp = True
        self.extremum = None

    def next(self):
        """
        zig转向交易策略系统的策略。
        Description :
        Arg :
        Returns :
        Raises	 :
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
    cerebro.addstrategy(Strategy_ZIG)
    # Set our desired cash start
    cerebro.set_cash(10000.0)
    #  run
    results = cerebro.run()
    # 显示分析师的结果
    cerebro.show_analyzer(results)
    # 用图表显示结果
    cerebro.show_plot()
