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

# 这个测试是看看5日均线穿越10日均线

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     # filename=os.path.join(file_dir,"app.log")
#     )
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
sys.path.append(os.path.join(file_dir, '../../../DataSource/baostock'))
import datasource as DataSource
sys.path.append(os.path.join(file_dir, '../../../'))
import Utils
# 这个是筛选多少天上涨多少的，
codes = DataSource.get_codes()
logger.debug(f'股票数量:{len(codes)},第一支股票:{codes[0]}')
# code = codes[0]
# dt = datasource.getData(code)
# dt.head() 

import pandas as pd
SHORT = 5
LONG = 10
STOP_LOSS = 0.05
class TenDayMASLStrategy(backtrader.Strategy):
    """
    10日均线交易策略，包含固定百分比止损。
    买入: 收盘价 > 10日均线
    卖出: 1) 收盘价 < 10日均线； 2) 从买入价下跌10%止损
    """
    params = (
        ('short', SHORT),      # 均线周期
        ('long', LONG),      # 均线周期
        ('stop_loss', STOP_LOSS),    # 止损比例 (10%)
    )

    def __init__(self):
        # 初始化10日简单移动平均线
        self.sma1 = backtrader.ind.SmoothedMovingAverage(self.data, period=self.params.short)
        self.sma2 = backtrader.ind.SmoothedMovingAverage(self.data, period=self.params.long)
        self.sar = backtrader.ind.ParabolicSAR(self.data)
        # 交叉的
        self.cross = backtrader.ind.CrossOver(self.sma1, self.sma2)
        # 用于记录买入订单和买入价格
        self.order = None
        self.buyprice = None
        self.debug(f'初始化完毕')

    def next(self):
        # 如果已有订单 pending，则不再发新订单
        if self.order:
            return

        # 检查是否持有仓位
        if not self.position:
            # **买入条件: 收盘价上穿10日均线，这里暂时没有考虑止损**
            if self.cross[0] > 0 and self.data.close[0] > self.sar[0]:
                self.order = self.order_target_percent(target=0.9) # 每次都0.9个
       
        else:
            # **卖出条件1: 收盘价跌破日均线 (趋势结束)**
            sell_cond1 = self.data.close[0] < self.sma2[0]
            # **卖出条件2: 当前价格较买入价下跌超过止损比例 (风险控制)**
            sell_cond2 = False
            if self.buyprice:
                sell_cond2 = self.data.close[0] < self.buyprice * (1 - self.params.stop_loss)
            # **卖出条件3，均线死叉
            sell_cond3 = self.cross[0] < 0
            # **卖出条件4，止损抛物sar
            sell_cond4 = self.sar[0] > self.data.close[0]
            # !触发任一卖出条件则执行卖出
            sell_conds = [sell_cond1, sell_cond2, sell_cond3, sell_cond4]
            sell_conds = [i for i in sell_conds if i ]
            if len(sell_conds)>0:
                # reason = '跌破均线' if sell_cond1 else f'触发{self.params.stop_loss*100:.0f}%止损'
                # self.log(f'SELL CREATE ({reason}), Price: {self.data.close[0]:.2f}, Cost: {self.buyprice:.2f}')
                # 卖出全部持仓
                self.order = self.close()

    def notify_order(self, order):
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
                self.debug(f'BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:6.2f}, 佣金Comm: {order.executed.comm:.2f},订单完成后 -> 现金: {current_cash:.2f}, 总资产: {portfolio_value:.2f}')
            else:
                # 卖出订单完成，重置买入成本价
                self.debug(f'SELL EXECUTED, buy price:{self.buyprice}, sell Price: {order.executed.price:.2f}, Cost: {order.executed.value:6.2f}, 佣金Comm: {order.executed.comm:.2f},订单完成后 -> 现金: {current_cash:.2f}, 总资产: {portfolio_value:.2f}')
                self.buyprice = None
                
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.debug('Order Canceled/Margin/Rejected')

        # 重置主订单变量
        self.order = None

    def debug(self, txt, dt=None, doprint=True):
        '''策略日志函数'''
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            # print(f'{dt.isoformat()}, {txt}')
            logger.debug(f'{dt.isoformat()}, {txt}')
    
    def info(self, txt, dt=None, doprint=True):
        '''策略日志函数'''
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            # print(f'{dt.isoformat()}, {txt}')
            logger.info(f'{dt.isoformat()}, {txt}')

# 以下是回测引擎的设置示例 (需与您的数据配合使用)
if __name__ == '__main__':
    init_amount = 10000.0 # 初始的金额
    logger.info(f'初始金额:{init_amount}')
    code_value = [] # 用这个数组来保存股票的收益情况
    for i in range(len(codes)):
        try:
            # 创建大脑引擎
            cerebro = backtrader.Cerebro()
            # 添加策略
            cerebro.addstrategy(TenDayMASLStrategy, short=SHORT, long=LONG,stop_loss=STOP_LOSS)
            # 加载数据 (请替换为您的数据路径和格式)
            # 假设数据为CSV，格式示例：日期,开盘,最高,最低,收盘,成交量
            code = codes[i]
            # 这里只是看看上海和深圳掌权交易所的
            if code.startswith('00')or code.startswith('60'):
                logger.debug(f'******开始回测股票:{code}******')
                data2 = DataSource.getData(code)
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
                # 运行回测
                cerebro.run()
                logger.info(f'{code}最终资金: {cerebro.broker.getvalue():.2f}')
                code_value.append((code, cerebro.broker.getvalue())) # 记录结果
        except Exception as err:
            msg = str(err)
            logger.error(msg)
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
    logger.info(f'短：{SHORT},长：{LONG}, 止损:{STOP_LOSS},收益平均值:{values.mean()},方差:{values.std()},中位值:{values.median()},最大值：{values.max()},最小值：{values.min()}')
    end = datetime.datetime.now()
    logger.info(f"运行时间： {end - start}")