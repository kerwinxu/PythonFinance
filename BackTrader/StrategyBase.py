#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-10-08 10:30:59
# Last Change:  2017-12-17 23:19:21
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
        if order.status in [order.Completed]:
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
            elif order.issell():  # Sell
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
            self.log('Order Canceled/Margin/Rejected', isprint=True)
        #  重置单子标志
        self.order = None

    def stop(self):
        pass

    def get_max_sizing(self, price=None):
        """
            Description : 取得可以购买的最大数量。
                算法是先取得现金金额, 然后取得杠杆，算出可以购买的最大

            Arg :

            Returns :

            Raises	 :

        """
        # 获得现金
        _cash = self.broker.get_value()
        # 获得杠杆
        _leverage = self.broker.comminfo[None].get_leverage()
        # 获得价格
        _price = price
        if(_price is None):
            # 如果没有价格，就用收盘价计算吧。
            _price = self.data_close[0]
        # 简单计算，然后返回一个整形吧。
        return int(_cash * _leverage / _price)

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
        if(f < 0.1):
            return 0.1
        if(f > 0.4):
            return 0.4

        return f

    def get_right_sizing(self):
        """
            Description : 取得一个合适的尺寸

            Arg :

            Returns :

            Raises	 :

        """
        _size = int(self.get_max_sizing() * self.get_kally_ratio())
        if _size < 1:
            _size = 1
        return _size
        pass

    def buy_add(self):
        """
            Description : 判断是否可以加仓，

            Arg :

            Returns :

            Raises	 :

        """
        # 如果没有，就直接退出吧。
        if self.dict_open is None:
            return
        # 判断是否有价格被超过
        _price = []
        _close = self.data.close[0]
        for _p in self.dict_open.keys():
            if(_close > _p):
                _price.append(_p)
                self.order = self.buy(size=self.dict_open[_p])

        # 如果有被超过的
        for _p in _price:
            # 然后删除这个价格啦，已经完成使命了
            self.dict_open.pop(_p)

    def sell_add(self):
        """
            Description : 判断是否可以加仓，

            Arg :

            Returns :

            Raises	 :

        """
        # 如果没有，就直接退出吧。
        if self.dict_open is None:
            return
        # 判断是否有价格被超过
        _price = []
        _close = self.data.close[0]
        for _p in self.dict_open.keys():
            if(_close < _p):
                _price.append(_p)
                self.order = self.sell(size=self.dict_open[_p])

        # 如果有被超过的
        for _p in _price:
            # 然后删除这个价格啦，已经完成使命了
            self.dict_open.pop(_p)
