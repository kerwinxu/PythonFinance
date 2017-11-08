#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-11-07 21:20:35
# File Name: sample1.py

# import datetime  # For datetime objects
# import os.path  # To manage paths
# import sys  # To find out the script name (in argv[0])
# import pandas as pd
# from WindPy import w
# Import the backtrader platform
import backtrader as bt
import sys
sys.path.append("../FinanceDataSource")
import FinanceDataSource


# Create a Stratey
# 这个是均线系统，我大选系统如下：
# 当五日均线突破10日均线的时候，10%仓位
# 当MACD出现突破的时候，10%仓位。
class Strategy_MA(bt.Strategy):

    params = (
        ('ma1', 6),
        ('ma2', 12),
        ('ma3', 20),
        ('percent_order_1', 30),
        ('percent_order_2', 20),
        ('printlog', False)
    )

    def log(self, txt, dt=None, isprint=False):
        ''''' Logging function fot this strategy'''
        if self.params.printlog or isprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 添加多条均线
        self.sma1 = bt.talib.SMA(self.data, timeperiod=self.params.ma1)
        self.sma2 = bt.talib.SMA(self.data, timeperiod=self.params.ma2)
        self.sma3 = bt.talib.SMA(self.data, timeperiod=self.params.ma3)
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
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.opsize = order.executed.size
            else:  # Sell
                self.log('SELL EXECUTED, %d, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.size,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm))

    def stop(self):
        self.log('(%d,  %d)(%d, %d) Ending Value %.2f' %
                 (self.params.ma1, self.params.ma2, self.params.percent_order_1, self.params.percent_order_2, self.broker.getvalue()), isprint=True)

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
    cerebro = bt.Cerebro()

    # Add a strategy
    # 在这里加上我的策略，从
    cerebro.addstrategy(Strategy_MA)
    # cerebro.optstrategy(Strategy_MA,
    #                     ma1=6,
    #                     ma2=12,
    #                     percent_order_1=range(10, 30),
    #                     percent_order_2=range(10, 20)
    #                     )
    # 设置佣金杠杆
    # 上海黄金交易所手续费为万分之8，白银的递延费为万分之1.5， * 362 = 0.05475，这里不考虑杠杆。
    cerebro.broker.setcommission(commission=0.0008, interest=0.05475)

    # Create a Data Feed
    # parase_dates = True是为了读取csv为dataframe的时候能够自动识别datetime格式的字符串，big作为index
    # 注意，这里最后的pandas要符合backtrader的要求的格式
    dataframe = FinanceDataSource.get_data(FinanceDataSource.str_tonghuashun, FinanceDataSource.tonghuashun_AGTD)
    dataframe['openinterest'] = 0
    data = bt.feeds.PandasData(dataname=dataframe)
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # 每股固定10个
    # cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

    # 加入分析师
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AnnualReturn')
    cerebro.addanalyzer(bt.analyzers.Calmar, _name='Calmar')
    # cerebro.addanalyzer(bt.analyzers.PeriodStats, _name='PeriodStats')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='Returns')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='SQN')

    # Set our desired cash start
    cerebro.broker.setcash(50000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    results = cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Plot the result
    # cerebro.plot()

    # 显示分析师结果
    strat = results[0]
    # print('夏普比率:', strat.analyzers.SharpeRatio.get_analysis())
    # print('最大回撤:', strat.analyzers.DW.get_analysis())
    # print('年度回撤：', strat.analyzers.AnnualReturn.get_analysis())
    # print('Calmar：', strat.analyzers.Calmar.get_analysis())
    # print('PeriodStats：', strat.analyzers.PeriodStats.get_analysis())
    # print('年化收益：', strat.analyzers.Returns.get_analysis())
    # print('TradeAnalyzer：', strat.analyzers.TradeAnalyzer.get_analysis())
    # print('SQN指数：', strat.analyzers.SQN.get_analysis())
