# 这个文件可以被别的调用，
import pandas as pd
import numpy as np
import matplotlib
# matplotlib.use('agg')
import matplotlib.pyplot as plt
import os
# from tqdm.notebook import  tqdm
from tqdm import  tqdm
import talib
import datetime
import math
import  mplfinance as mpf
import backtrader
import logging

file_dir = os.path.dirname(os.path.realpath(__file__))
file_name = os.path.basename(__file__)
file_name_without_extension = os.path.splitext(file_name)[0]

import datetime
start = datetime.datetime.now()

# 这个测试是看看只要多日都在均线上。
# 创建一个 logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # 设置日志级别
 
# 创建一个文件处理器，用于写入日志文件
file_handler = logging.FileHandler(os.path.join(file_dir,f"{file_name_without_extension}-app.log"))
file_handler.setLevel(logging.DEBUG)  # 设置文件日志级别
 
# 创建一个控制台处理器，用于输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 设置控制台日志级别
 
# 创建一个文件日志格式器
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
 
# 创建一个控制台日志格式器
console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
 
# 将处理器添加到 logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


import sys
sys.path.append(os.path.join(file_dir, '../../DataSource/baostock'))
import datasource as DataSource
sys.path.append(os.path.join(file_dir, '../../'))
import Utils
# 这个是筛选多少天上涨多少的，
codes = DataSource.getStockIndustry()['code'].tolist()
logger.debug(f'股票数量:{len(codes)},第一支股票:{codes[0]}')

import backtrader as bt

# 只是增加了日志通知，
class StrategyLog(bt.Strategy):
    
    def __init__(self):
        # 用于记录买入订单和买入价格
        self.order = None
        self.buyprice = None
    
    def notify_order(self, order):
        # 订单变动通知。
        if order.status in [order.Submitted, order.Accepted]:
            # 订单已提交/接受 - 无需行动
            return
        # 查询并记录成交后的账户状况
        current_cash = self.broker.getcash()      # 当前可用现金
        portfolio_value = self.broker.getvalue()  # 当前总资产（现金+持仓市值）
        if order.status in [order.Completed]:
            if order.isbuy():
                # 买入订单完成，记录买入成本价
                self.buyprice = order.executed.price
                self.logDebug(f'BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:6.2f}, 佣金Comm: {order.executed.comm:.2f},订单完成后 -> 现金: {current_cash:.2f}, 总资产: {portfolio_value:.2f}')
            else:
                # 卖出订单完成，重置买入成本价
                self.logDebug(f'SELL EXECUTED, buy price:{self.buyprice}, sell Price: {order.executed.price:.2f}, Cost: {order.executed.value:6.2f}, 佣金Comm: {order.executed.comm:.2f},订单完成后 -> 现金: {current_cash:.2f}, 总资产: {portfolio_value:.2f}')
                self.buyprice = None
                
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.logDebug('Order Canceled/Margin/Rejected')

        # 重置主订单变量
        self.order = None
    
    def logError(self, txt, dt=None, doprint=True):
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            # print(f'{dt.isoformat()}, {txt}')
            logger.error(f'{dt.isoformat()}, {txt}')

    def logDebug(self, txt, dt=None, doprint=True):
        '''策略日志函数'''
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            # print(f'{dt.isoformat()}, {txt}')
            logger.debug(f'{dt.isoformat()}, {txt}')
    
    def logInfo(self, txt, dt=None, doprint=True):
        '''策略日志函数'''
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            # print(f'{dt.isoformat()}, {txt}')
            logger.info(f'{dt.isoformat()}, {txt}')



def testStrategy(stratety:bt.Strategy):
    '''测试交易的，参数是交易系统类'''
    init_amount = 10000.0 # 初始的金额
    logger.info(f'初始金额:{init_amount}')
    code_value = [] # 用这个数组来保存股票的收益情况
    for i in range(len(codes)):
        try:
            # 创建大脑引擎
            cerebro = backtrader.Cerebro()
            # 添加策略
            cerebro.addstrategy(stratety)
            # 加载数据 (请替换为您的数据路径和格式)
            # 假设数据为CSV，格式示例：日期,开盘,最高,最低,收盘,成交量
            code = codes[i]
            # 这里只是看看上海和深圳证券交易所的

            logger.debug(f'******开始回测股票:{code}******')
            data2 = DataSource.getData(code)
            # 至少有200个交易日才处理
            if len(data2)>200 and (code.startswith('sh.60') or code.startswith('sz.000') or code.startswith('sz.001')):
                # 这里需要将索引改成列明，也要删除空列
                data2 = data2.dropna().reset_index().rename(columns={'index': 'date'})
                data = backtrader.feeds.PandasData(dataname=data2,
                                        datetime='date',      # 指定日期时间列名
                                        open='open',          # 指定开盘价列名
                                        high='high',         # 指定最高价列名
                                        low='low',           # 指定最低价列名
                                        close='close',       # 指定收盘价列名
                                        volume='volume',     # 指定成交量列名
                                        )
                cerebro.adddata(data)
                
                # 设置初始资金和交易成本
                cerebro.broker.setcash(init_amount)  # 1万元初始资金
                # 设置固定交易手数：1手=100股
                cerebro.addsizer(backtrader.sizers.FixedSize, stake=100)
                cerebro.broker.setcommission(commission=0.001)  # 0.1%佣金
                cerebro.addanalyzer(backtrader.analyzers.SharpeRatio, _name = 'SharpeRatio') # 夏普
                cerebro.addanalyzer(backtrader.analyzers.DrawDown, _name='DW') # 回撤
                cerebro.addanalyzer(backtrader.analyzers.TradeAnalyzer, _name='ta') # 交易分析
                # 运行回测
                results = cerebro.run()
                strat = results[0]
                _sp = strat.analyzers.SharpeRatio.get_analysis().get('sharperatio', 'N/A')
                _dw_value = strat.analyzers.DW.get_analysis()['max']['drawdown']
                _dw_len = strat.analyzers.DW.get_analysis()['max']['len']
                ta = strat.analyzers.ta.get_analysis()
                # 要显示的消息。
                lst_msg = [
                    f'{code}',
                    f'最终资金: {cerebro.broker.getvalue():8.2f}',
                    f' 夏普比率:{_sp:8.2f}',
                    f'最大回撤指标:{_dw_value:8.2f}',
                    f'回撤周期:{_dw_len:4d}',
                    f'总交易次数: {ta.total.total:5d}',
                    f'盈利次数: {ta.won.total:5d}',
                    f'亏损次数: {ta.lost.total:5d}',
                    f'胜率: {ta.won.total / ta.total.total:2.2%}'           
                ]
                logger.info(','.join(lst_msg))
                code_value.append((code, cerebro.broker.getvalue())) # 记录结果
        except Exception as err:
            msg = str(err)
            logger.error(f"{code}:" + msg)
            pass  
        # 可视化回测结果
        # cerebro.plot(style='candlestick')
    # 这里进行保存
    df = pd.DataFrame({
        'code':[i[0] for i in code_value],
        'value':[i[1] for i in code_value]
    })
    df.to_csv(os.path.join(file_dir,f'{file_name_without_extension}-result.csv'))
    # 我这里想要看看平均值，最大值，最小值和均方差
    values = df['value']
    logger.info(f'收益平均值:{values.mean()},方差:{values.std()},中位值:{values.median()},最大值：{values.max()},最小值：{values.min()}')
    end = datetime.datetime.now()
    logger.info(f"运行时间： {end - start}")