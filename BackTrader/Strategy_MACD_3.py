#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-12-19 22:58:35
# File Name: sample1.py
import backtrader as bt
import CerebroBase
import StrategyBase


# Create a Stratey
# 这个MACD系统
class Strategy_MACD(StrategyBase.StrategyBase):
    '''
    This strategy is loosely based on some of the examples from the Van
    K. Tharp book: *Trade Your Way To Financial Freedom*. The logic:

      - Enter the market if:
        - The MACD.macd line crosses the MACD.signal line to the upside
        - The Simple Moving Average has a negative direction in the last x
          periods (actual value below value x periods ago)

     - Set a stop price x times the ATR value away from the close

     - If in the market:

       - Check if the current close has gone below the stop price. If yes,
         exit.
       - If not, update the stop price if the new stop price would be higher
         than the current
    '''

    params = (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('atrperiod', 14),  # ATR Period (standard)
        ('atrdist', 2),   # ATR distance for stop price
        ('smaperiod', 30),  # SMA Period (pretty standard)
        ('dirperiod', 10),  # Lookback period to consider SMA trend direction
        ('atr_open', 0.5), # 我计算出每个加仓位置，这里表示多少个ATR。
        ('ratio1', 0.2),
        ('ratio2', 0.1),
        ('ratio3', 0.1),
        ('ratio4', 0.1),
    )


    def __init__(self):
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)

        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        # To set the stop price
        # 今日振幅、今日最高与昨收差价，今日最低与昨收差价中的最大值，为真实波幅，
        self.atr = bt.indicators.ATR(self.data, period=self.p.atrperiod)

        # Control market trend
        self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)
        self.smadir = self.sma - self.sma(-self.p.dirperiod)

        self.order = None  # sentinel to avoid operrations on pending order
        self.dict_open = {}

    def next(self):
        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market
            _max_size = self.get_max_sizing()
            _close = self.data.close[0]
            _size_1 = int(_max_size * self.params.ratio1)
            _size_2 = int(_max_size * self.params.ratio2)
            _size_3 = int(_max_size * self.params.ratio3)
            _size_4 = int(_max_size * self.params.ratio4)
            if self.mcross[0] > 0.0 and self.smadir < 0.0:
                # 开仓
                self.order = self.buy(size=_size_1)
                # 记录止损位置
                pdist = self.atr[0] * self.p.atrdist
                self.pstop = _close - pdist
                # 然后计算所有的几个加仓位置
                # 我用字典来表示吧，键名为价格，键值为要买的点数
                self.dict_open = {}
                # 用金字塔式加仓
                # 分别在如下位置加仓
                _price_2 = _close + 1 * self.atr[0] * self.params.atr_open
                _price_3 = _close + 2 * self.atr[0] * self.params.atr_open
                _price_4 = _close + 3 * self.atr[0] * self.params.atr_open
                # 做加仓字典
                self.dict_open[_price_2] = _size_2
                self.dict_open[_price_3] = _size_3
                self.dict_open[_price_4] = _size_4
            # elif self.mcross[0] < 0.0 :
                # # 开仓
                # self.order = self.sell(size=_size_1)
                # # 记录止损位置
                # pdist = self.atr[0] * self.p.atrdist
                # self.pstop = _close + pdist
                # # 然后计算所有的几个加仓位置
                # # 我用字典来表示吧，键名为价格，键值为要买的点数
                # self.dict_open = {}
                # # 用金字塔式加仓
                # # 分别在如下位置加仓
                # _price_2 = _close - 1 * self.atr[0] * self.params.atr_open
                # _price_3 = _close - 2 * self.atr[0] * self.params.atr_open
                # _price_4 = _close - 3 * self.atr[0] * self.params.atr_open
                # # 做加仓字典
                # self.dict_open[_price_2] = _size_2
                # self.dict_open[_price_3] = _size_3
                # self.dict_open[_price_4] = _size_4

        else:  # in the market
            # 如果是买单
            if self.position.size > 0:
                pclose = self.data.close[0]
                pstop = self.pstop

                if pclose < pstop:
                    self.close()  # stop met - get out
                else:
                    pdist = self.atr[0] * self.p.atrdist
                    # Update only if greater than
                    self.pstop = max(pstop, pclose - pdist)
                    self.buy_add()
            # elif self.position.size < 0:
                # pclose = self.data.close[0]
                # pstop = self.pstop

                # if pclose > pstop:
                    # self.close()  # stop met - get out
                # else:
                    # pdist = self.atr[0] * self.p.atrdist
                    # # Update only if greater than
                    # self.pstop = min(pstop, pclose + pdist)
                    # self.sell_add()


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = CerebroBase.CerebroAGTD()
    # Add a strategy
    cerebro.addstrategy(Strategy_MACD)
    # Set our desired cash start
    cerebro.set_cash(5000.0)
    cerebro.show_analyzer(cerebro.run())
    cerebro.show_plot()
