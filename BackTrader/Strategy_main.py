#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-10-08 10:30:59
# Last Change:  2017-10-08 16:18:24
# File Name: Strategy_main.py

import backtrader as bt


class StrategyBase(bt.Strategy):
    """
    这个类是作为交易类的基类来的，加上自己的一些东西，
    以便我继承后，我只用些next方法和__init__方法就可以了。
    """

    def log(self, txt, dt=None, isprint=False):
        ''''' Logging function fot this strategy'''
        if self.params.printlog or isprint:
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
                    'BUY EXECUTED, %d, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.size,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm), isprint=True)

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.opsize = order.executed.size
            else:  # Sell
                self.log('SELL EXECUTED, %d, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.size,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm
                          ), isprint=True)

    def stop(self):
        pass
