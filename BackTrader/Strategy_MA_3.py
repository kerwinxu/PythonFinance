#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-11-10 20:54:20
# File Name: sample1.py

import backtrader as bt
import CerebroBase
import StrategyBase

# Create a Stratey
# 这个是均线系统，我大选系统如下：
# 当五日均线突破10日均线的时候，10%仓位
# 当MACD出现突破的时候，10%仓位。
class Strategy_MA(StrategyBase.StrategyBase):

    params = (
        ('ma1', 6),
        ('ma2', 12),
        ('ma3', 20),
        ('percent_order_1', 30),
        ('percent_order_2', 20),
        ('printlog', False)
    )

    def __init__(self):
        # 添加多条均线
        self.sma1 = bt.talib.SMA(self.data, timeperiod=self.params.ma1)
        self.sma2 = bt.talib.SMA(self.data, timeperiod=self.params.ma2)
        self.sma3 = bt.talib.SMA(self.data, timeperiod=self.params.ma3)
        self.order = None
    def next(self):
        """我这里打算交易方法是用均线的方向来判断
        比如2条均线：
            我设置5 日均线涨是30%下单，跌是 -30%下单
            我设置10日均线涨是30%下单，跌是 -20%下单

        """
        # 这个就是要下单的比率
        percent_order = 0
        # 如下是取得几个均线数据
        ma1_now = self.sma1[0]
        ma1_pre = self.sma1[-1]
        ma2_now = self.sma2[0]
        ma2_pre = self.sma2[-1]
        # 因为这个是回测昨天的，所以我以开盘价为准吧，不方便添加止损啊。
        # open_price = self.data_open[0]

        if ma1_now > ma1_pre:
            percent_order = percent_order + self.params.percent_order_1/100
        else:
            percent_order = percent_order - self.params.percent_order_1/100

        if ma2_now > ma2_pre:
            percent_order = percent_order + self.params.percent_order_2/100
        else:
            percent_order = percent_order - self.params.percent_order_2/100

        # 然后根据百分比下单
        # 这个不方便下止损单。
        self.order = self.order_target_percent(target=percent_order)
        """
        # 取得当前的单子信息
        # current_price = self.position.price
        current_size = self.position.size

        # 获得总资产
        value = self.broker.get_value()
        # 需要调整到的尺寸
        need_size = value / open_price * percent_order
        # 设置止损
        if (percent_order > 0):
            # 到这里就是买单
            if(current_size > 0):
                # 如果原先就有买单了
                # 那么先判断是否需要加仓
                if(need_size > current_size):
                    # 到这里需要加仓
                    self.order = self.buy_bracket(size=need_size-current_size, price=open_price, stopprice=open_price-100)
            else:
                # 到这里表示已经有卖单，得先平仓
                self.order = self.close()
                # 然后下单
                self.order = self.buy_bracket(size=need_size, price=open_price, stopprice=open_price-100)
        else:
            # 到这里就是下卖单
            if(current_size > 0):
                # 这里表示原先就已经有买单，得先平仓
                self.order = self.close()
                # 然后再下单
                self.order = self.sell_bracket(size=abs(need_size), price=open_price, stopprice=open_price+100)
            else:
                # 这里表示原先就有卖单，补仓就可以了
                self.order = self.sell_bracket(size=abs(need_size - current_size), price=open_price, stopprice=open_price+100)
                """
if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = CerebroBase.CerebroAGUSDO()
    # Add a strategy
    cerebro.addstrategy(Strategy_MA)
    # Set our desired cash start
    cerebro.set_cash(100000.0)
    cerebro.run()
