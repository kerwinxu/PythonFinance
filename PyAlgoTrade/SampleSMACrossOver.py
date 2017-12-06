#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name: helloworld.py
# Author:  kerwin.cn@gmail.com
# Created Time:2017-11-15 12:31:05
# Last Change:  2017-11-15 20:12:17
# Description :

from pyalgotrade import strategy
from pyalgotrade.bar import Frequency
# from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade import plotter
import os
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade.stratanalyzer import returns
# 1.构建一个策略


class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(SMACrossOver, self).__init__(feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, smaPeriod)

    def getSMA(self):
        return self.__sma

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0:
                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma) > 0:
            self.__position.exitMarket()

# 2.获得回测数据，官网来源于yahoo，由于墙的关系，我们用本地数据
# feed = GenericBarFeed(Frequency.DAY, None, None)
feed = yahoofeed.Feed(Frequency.DAY, None, None)
csf_file_name = os.path.join(os.path.dirname(__file__), "yahoo_^DJI.csv")
feed.addBarsFromCSV("fd", csf_file_name)

# Evaluate the strategy with the feed's bars.
myStrategy = SMACrossOver(feed, "fd", 20)

# Attach a returns analyzers to the strategy.
returnsAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(returnsAnalyzer)

# Attach the plotter to the strategy.
plt = plotter.StrategyPlotter(myStrategy)
# Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
plt.getInstrumentSubplot("fd").addDataSeries("SMA", myStrategy.getSMA())
# Plot the simple returns on each bar.
plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

# Run the strategy.
myStrategy.run()
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

# Plot the strategy.
plt.plot()
