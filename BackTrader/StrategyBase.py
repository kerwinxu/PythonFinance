#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-10-08 10:30:59
# Last Change:  2017-12-14 10:00:59
# File Name: Strategy_main.py

import backtrader as bt


class StrategyBase(bt.Strategy):
    """
    这个类是作为交易类的基类来的，加上自己的一些东西，
    以便我继承后，我只用些next方法和__init__方法就可以了。
    """

    def log(self, txt, dt=None, isprint=False):
        ''''' Logging function fot this strategy'''
        if isprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.order = None

    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, %d, Price: %.2f, Value: %.2f, Comm : %.2f, current value : %.2f, current cash : %.2f' %
                    (order.executed.size,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm,
                     self.broker.get_value(),
                     self.broker.get_cash()
                     ), isprint=True)

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.opsize = order.executed.size
            else:  # Sell
                self.log('SELL EXECUTED, %d, Price: %.2f, Value: %.2f, Comm : %.2f , current value : %.2f , current cash : %.2f' %
                         (order.executed.size,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                          self.broker.get_value(),
                          self.broker.get_cash()
                          ), isprint=True)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        #  重置单子标志
        self.order = None
        # 显示有多少钱

    def stop(self):
        pass

    def get_kally_ratio(self, b=None, p=None):
        """
            Description : 获得凯莉公式计算开仓大小
                凯莉公式计算 (bp-q)/b
            Arg :
                @b : 赔率
                @p : 获胜的概率
            Returns : 应该投注的比值

            Raises	 :

        """
        _analysis= self.analyzers.TradeAnalyzer.get_analysis()
        if(b==None):
            # 如果赔率空值，就表示得从以往的交易中获得
            try:
                _won_avg = _analysis['won']['pnl']['average']
                _lost_avg = _analysis['lost']['pnl']['average']
                b = abs(_won_avg / _lost_avg)
                pass
            except:
                # 默认赔率为1
                b = 1
            if b <= 0:
                b = 1
        if(p==None):
            # 如果获胜的概率为空值，也表示得从以往的交易中获得
            try:
                _won_count = _analysis['won']['total']
                _lost_count = _analysis['lost']['total']
                p = _won_count / (_won_count + _lost_count)
                pass
            except:
                # 默认有20%的成功率就足够高了
                p = 0.20
                pass
        # 失败的概率
        q = 1 - p
        f = (b * p - q)/b
        # 判断f的范围

        if(f < 0):
            return 0.1

        return f
