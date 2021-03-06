#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-11-08 19:26:07
# Last Change:  2018-01-07 20:59:22
# File Name: CerebroBase.py

import backtrader as bt
import sys
import os
sys.path.append(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        "../FinanceDataSource"))
import FinanceDataSource


class CerebroBase(object):
    """
    这个类是我做的大脑的基类，主要为了少些代码
    """

    def __init__(self):
        """这个会调用backtrader的Crrebr来实现功能"""
        self.cerebro = bt.Cerebro()
        # 分析师
        self.analyzers = []
        # 加入分析师
        self.init_analyzers()

    def addstrategy(self, strategy_, *args, **kwargs):
        """设置策略"""
        self.cerebro.addstrategy(strategy_, *args, ** kwargs)

    def adddata(self, data_, name=None):
        """设置数据"""
        self.cerebro.adddata(data_, name=name)

    def set_cash(self, cash_=10000):
        """设置起始金额，默认为10000"""
        self.cerebro.broker.set_cash(cash_)

    def addanalyzer(self, analyzer, analyzer_name):
        """添加分析师
        然后保存分析师，以备输出结果"""
        self.cerebro.addanalyzer(analyzer, _name=analyzer_name)
        self.analyzers.append(analyzer_name)

    def init_analyzers(self):
        """初始化分析师的"""
        self.addanalyzer(bt.analyzers.Calmar, 'Calmar') # 收益和最大回撤之间的关系。
        self.addanalyzer(bt.analyzers.DrawDown, 'DW')
        self.addanalyzer(bt.analyzers.AnnualReturn, 'AnnualReturn')
        self.addanalyzer(bt.analyzers.PeriodStats, 'PeriodStats')   # Calculates basic statistics for given timeframe
        self.addanalyzer(bt.analyzers.Returns, 'Returns')
        self.addanalyzer(bt.analyzers.TradeAnalyzer, 'TradeAnalyzer')
        self.addanalyzer(bt.analyzers.SQN, 'SQN')   # 交易次数N的平方根 * 交易系统的期望值 / 期望值的标准差
        self.addanalyzer(bt.analyzers.SharpeRatio, 'SharpeRatio') # 夏普比率

    def show_analyzer(self, results):
        # 显示分析师结果
        strat = results[0]
        len(strat)
        for value in self.analyzers:
            a = "strat.analyzers.%s.get_analysis()" % value
            b = eval(a)
            print("{0}:{1}".format(value, b))

    def run(self):
        """这个会运行，且显示图表和分析结果"""
        # 运行
        results = self.cerebro.run()
        # 返回运行结果
        return results

    def show_plot(self):
        self.cerebro.plot()


class CerebroAGUSDO(CerebroBase):
    """这个是伦敦银的测试大脑"""

    def init_data(self):
        """封装上数据"""
        dataframe = FinanceDataSource.get_data(
            FinanceDataSource.str_tonghuashun,
            FinanceDataSource.tonghuashun_AGUSDO)
        dataframe['openinterest'] = 0
        data = bt.feeds.PandasData(dataname=dataframe)
        self.adddata(data)

    def __init__(self):
        super(CerebroAGUSDO, self).__init__()
        self.init_data()
        pass


class CerebroAGTD(CerebroBase):
    """这个是封装上海黄金交易所的白银TD"""

    def __init__(self):
        super(CerebroAGTD, self).__init__()
        dataframe = FinanceDataSource.get_data(
            FinanceDataSource.str_tonghuashun,
            FinanceDataSource.tonghuashun_AGTD)
        dataframe['openinterest'] = 0
        data = bt.feeds.PandasData(dataname=dataframe)
        self.adddata(data)
        # 如下是佣金
        self.cerebro.broker.setcommission(
            # automargin=0.15,  # 保证金比例
            commission=0.0008,  # 手续费，记得是万分之8
            leverage = 100/15,  # 这个才是真正的杠杆，15%的保证金相当于100 / 15的杠杆
            interest=0.073  # 递延费，记得是万分之8， * 365 = 0.073
        )


class CerebroAUTD(CerebroBase):
    """这个是封装的是上海黄金交易所的黄金TD"""

    def __init__(self):
        super(CerebroAUTD, self).__init__()
        dataframe = FinanceDataSource.get_data(
            FinanceDataSource.str_tonghuashun,
            FinanceDataSource.tonghuashun_AUTD)
        dataframe['openinterest'] = 0
        data = bt.feeds.PandasData(dataname=dataframe)
        self.adddata(data)
        # 如下是佣金
        self.cerebro.broker.setcommission(
            # automargin=0.15,  # 保证金比例
            commission=0.0008,  # 手续费，记得是万分之8
            leverage = 100/15,  # 这个才是真正的杠杆，15%的保证金相当于100 / 15的杠杆
            interest=0.073,   # 递延费，记得是万分之8， * 365 = 0.073
            # mult = 100, # 这个应该是一手是多少克吧, 但是却不成功。
            # automargin = -1,    # Use param mult * price if automargin < 0 , 不能实现一手是100克。

        )

class CereborAGE(CerebroBase):
    """
    我封装的上海黄金交易所信息。
    Attributes	:
    functions	:

    """
    def __init__(self):
        super(CereborAGE, self).__init__()

        dataframe_AUTD = FinanceDataSource.get_data(
            FinanceDataSource.str_tonghuashun,
            FinanceDataSource.tonghuashun_AUTD)
        dataframe_AGTD = FinanceDataSource.get_data(
            FinanceDataSource.str_tonghuashun,
            FinanceDataSource.tonghuashun_AGTD)

        dataframe_AUTD['openinterest'] = 0
        dataframe_AGTD['openinterest'] = 0

        data_AUTD = bt.feeds.PandasData(dataname=dataframe_AUTD)
        data_AGTD = bt.feeds.PandasData(dataname=dataframe_AGTD)

        self.adddata(data_AUTD, name="AUTD")
        self.adddata(data_AGTD, name="AGTD")
        # 如下是佣金
        self.cerebro.broker.setcommission(
            # automargin=0.15,  # 保证金比例
            commission=0.0008,  # 手续费，记得是万分之8
            leverage = 100/15,  # 这个才是真正的杠杆，15%的保证金相当于100 / 15的杠杆
            interest=0.073,   # 递延费，记得是万分之8， * 365 = 0.073
            # mult = 100, # 这个应该是一手是多少克吧, 但是却不成功。
            # automargin = -1,    # Use param mult * price if automargin < 0 , 不能实现一手是100克。
        )

