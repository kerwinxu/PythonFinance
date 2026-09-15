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
from multiprocessing import Pool
from itertools import product

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

# 这里钻诚聚宽的数据
import sys
sys.path.append(os.path.join(file_dir, '../../DataSource/聚宽数据'))
import datasource as DataSource
# sys.path.append(os.path.join(file_dir, '../../'))
# import Utils
# 这个是筛选多少天上涨多少的，
codes = DataSource.getAStockCodes()
logger.debug(f'股票数量:{len(codes)},第一支股票:{codes[0]}')

import backtrader as bt

# 只是增加了日志通知，
class StrategyLog(bt.Strategy):
    
    def __init__(self):
        # 用于记录买入订单和买入价格
        self.order = None # 保存订单
        self.buyprice = None # 买价
        self.order_creation_time = None # 开仓时间
        self.order_creation_time_s = []
        self.logDebug(f'初始化完毕')
    
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
                self.order_creation_time = order.created.dt
                self.logDebug(f'BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:6.2f}, 佣金Comm: {order.executed.comm:.2f},订单完成后 -> 现金: {current_cash:.2f}, 总资产: {portfolio_value:.2f}')
            else:
                # 卖出订单完成，重置买入成本价
                # 这里取得时间
                if hasattr(order, 'executed'):
                    completion_time = order.executed.dt
                elif hasattr(order, 'expired'):
                    completion_time = order.expired.dt
                # 持股天数
                holding_period = bt.num2date(completion_time) - bt.num2date(self.order_creation_time)
                self.order_creation_time_s.append(holding_period)
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

class HoldingPeriodAnalyzer(bt.Analyzer):
    """自定义的分析持股天数的

    Args:
        bt (_type_): _description_
    """
    def __init__(self):
        self.trade_records = []  # 存储每笔交易的持仓时间
        self.trade_percent_records = [] # 交易后的盈利百分比
        self.last_size = 0 # 记录开仓

    def next(self):
        pass  # 不需要在每个 bar 中执行操作

    def notify_trade(self, trade):
        if trade.isclosed:  # 当交易关闭时
            # 持股天数的分析
            open_date = bt.num2date(trade.dtopen)  # 转换为 datetime 对象
            close_date = bt.num2date(trade.dtclose)
            holding_days = (close_date - open_date).days  # 计算持仓天数
            self.trade_records.append(holding_days)
            # 盈利亏损的百分比
            pnl = trade.pnlcomm # 扣除佣金后的金额
            size = self.last_size - trade.size 
            self.last_size = trade.size # 现在手里的数量
            price = trade.price
            if size * price == 0:
                return  # 避免除以零
            else:
                profit_pct = (pnl / (size * price)) * 100 # 盈利亏损的百分比
                self.trade_percent_records.append(profit_pct)
        elif trade.isopen:
            self.last_size += trade.size # 增加交易数量

    def get_analysis(self):
        return {
            'total_trades': len(self.trade_records),
            'average_holding_days': sum(self.trade_records) / len(self.trade_records) if self.trade_records else 0,
            'max_holding_days': max(self.trade_records) if self.trade_records else 0,
            'min_holding_days': min(self.trade_records) if self.trade_records else 0,
            'holding_days_list': self.trade_records,  # 所有交易的持仓天数列表
            'max_trade_percent': max(self.trade_percent_records) if len(self.trade_percent_records) > 0 else 0,
            'min_trade_percent': min(self.trade_percent_records) if len(self.trade_percent_records) > 0 else 0,
            'trade_percent_list': self.trade_percent_records,
        }


def testStrategy(stratety:bt.Strategy, file_path=None, file_out_name=None):
    """测试交易的，参数是交易系统类
    Args:
        stratety (bt.Strategy): 交易策略累
        file_path (_type_, optional): 外边调用的脚本路径. Defaults to None.
        file_out_name (_type_, optional): 保存的策略结果文件名称. Defaults to None.

    Returns:
        _type_: 策略结果
    """
    '''测'''
    # 这里做一下结果放在哪里
    if file_path is not None:
        file_dir = os.path.dirname(os.path.realpath(file_path))
        file_name = os.path.basename(file_path)
        file_name_without_extension = os.path.splitext(file_name)[0]
    if file_out_name is not None:
        file_name_without_extension = file_out_name
    # 添加日志，保存在
    file_handler2 = logging.FileHandler(os.path.join(file_dir,f"{file_name_without_extension}-app.log"))
    file_handler2.setFormatter(file_formatter)
    logger.addHandler(file_handler2)
    # 下边是策略
    init_amount = 10000.0 # 初始的金额
    logger.info(f'初始金额:{init_amount}')
    # 如下的是记录收益情况
    code_value = [] # 用这个数组来保存股票的收益情况
    for i in range(len(codes)):
        try:
            # 创建大脑引擎
            cerebro = backtrader.Cerebro(maxcpus=6)
            # 添加策略
            cerebro.addstrategy(stratety)
            # 加载数据 (请替换为您的数据路径和格式)
            # 假设数据为CSV，格式示例：日期,开盘,最高,最低,收盘,成交量
            code = codes[i]
            # 这里只是看看上海和深圳证券交易所的
            if code.startswith('30'):
                # 不做这个
                continue

            logger.debug(f'******开始回测股票:{code}******')
            data2 = DataSource.getData(code)
            # 至少有200个交易日才处理
            # if len(data2)>200 and (code.startswith('sh.60') or code.startswith('sz.000') or code.startswith('sz.001')):
            if len(data2)>200:
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
                cerebro.addanalyzer(HoldingPeriodAnalyzer, _name='holding_period')  # 添加持股天数分析器
                # 运行回测
                results = cerebro.run(tradehistory=True)
                strat = results[0]
                _sp = strat.analyzers.SharpeRatio.get_analysis().get('sharperatio', 'N/A')
                _dw_value = strat.analyzers.DW.get_analysis()['max']['drawdown']
                _dw_len = strat.analyzers.DW.get_analysis()['max']['len']
                ta = strat.analyzers.ta.get_analysis()
                holding_analysis = results[0].analyzers.holding_period.get_analysis()
                # 要显示的消息。
                lst_msg = [
                    f'{i+1}/{len(codes)}:'
                    f'{code}',
                    f'最终资金: {cerebro.broker.getvalue():8.2f}',
                    f' 夏普比率:{_sp:5.2f}',
                    f'最大回撤指标:{_dw_value:5.2f}',
                    f'回撤周期:{_dw_len:4d}',
                    f'总交易次数: {ta.total.total:3d}',
                    f'盈利次数: {ta.won.total:3d}',
                    f'最大盈利: {holding_analysis['max_trade_percent']:5.1f}%',
                    f'亏损次数: {ta.lost.total:3d}',
                    f'最大亏损: {holding_analysis['min_trade_percent']:5.1f}%',
                    f'胜率: {ta.won.total / ta.total.total:2.2%}',
                    f"平均持仓天数: {holding_analysis['average_holding_days']:3.1f} 天",
                    f"最大: {holding_analysis['max_holding_days']:3d} 天",
                    f"最小: {holding_analysis['min_holding_days']:3d} 天"
                ]
                logger.info(','.join(lst_msg))
                # 如下的是要保存到csv文件中
                code_value.append(
                    [
                        code,
                        cerebro.broker.getvalue(),
                        _sp,
                        _dw_value,
                        _dw_len,
                        ta.total.total,
                        ta.won.total,
                        holding_analysis['max_trade_percent'],
                        ta.lost.total,
                        holding_analysis['min_trade_percent'],
                        holding_analysis['average_holding_days'],
                        holding_analysis['max_holding_days'],
                        holding_analysis['min_holding_days']
                    ]
                )
        except Exception as err:
            msg = str(err)
            logger.error(f"{code}:" + msg)
            pass  
        # 可视化回测结果
        # cerebro.plot(style='candlestick')
    # 这里进行保存
    df = pd.DataFrame({
        'code':[i[0] for i in code_value],  # 股票代码
        'value':[i[1] for i in code_value], # 最终资金
        'sp':[i[2] for i in code_value], # 夏普比率
        'dw_value':[i[3] for i in code_value], # 最大回撤指标
        'dw_len':[i[4] for i in code_value], # 回撤周期
        'total':[i[5] for i in code_value], # 总的交易次数
        'won_total':[i[6] for i in code_value], # 盈利次数
        'won_max':[i[7] for i in code_value], # 最大盈利
        'lost_total':[i[8] for i in code_value], # 亏损次数
        'lost_max':[i[9] for i in code_value], # 最大亏损
        'avg_days':[i[10] for i in code_value], # 平均持股天数
        'max_days':[i[11] for i in code_value], # 最大持股天数
        'min_days':[i[12] for i in code_value] # 最低持股天数
    })
    df.to_excel(os.path.join(file_dir,f'{file_name_without_extension}-result.xlsx'))
    # 我这里想要看看平均值，最大值，最小值和均方差
    values = df['value']
    logger.info(f'收益平均值:{values.mean()},方差:{values.std()},中位值:{values.median()},最大值：{values.max()},最小值：{values.min()}')
    end = datetime.datetime.now()
    logger.info(f"运行时间： {end - start}")
    # 返回
    return df



def run_strategy(stratety:bt.Strategy,code:int | str | None=None, **params):
    """使用给定的参数进行单词回测

    Args:
        stratety (bt.Strategy): 策略
        code (int | str | None, optional): 序号或者股票代码. Defaults to None.
    """
    init_amount = 10000.0 # 初始的金额
    # 这里要判断一下取得哪个股票的
    _code = code
    if code is None:
        _code = codes[0] # 默认第一个股票
    elif isinstance(code, int):
        if code >= len(codes):
            logger.error(f'序号{code}超出')
            return
        _code = codes[code] # 当作序号
    elif isinstance(code, str):
        _code = code
        if _code not in codes:
            logger.error(f'无效的股票代码:{code}')
            return
    # 这里取得股票的数据
    data2 = DataSource.getData(_code)
    # 然后测试
    # 创建大脑引擎
    cerebro = backtrader.Cerebro()
    # 添加策略
    cerebro.addstrategy(stratety, **params)
    # 添加数据
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
    cerebro.addanalyzer(HoldingPeriodAnalyzer, _name='holding_period')  # 添加持股天数分析器
    results = cerebro.run()
    strat = results[0]

    sharpe = strat.analyzers.SharpeRatio.get_analysis().get('sharperatio', 0) or 0
    max_dd = strat.analyzers.DW.get_analysis()['max']['drawdown']
    final_value = cerebro.broker.getvalue()
    # 返回结果，这里要将params拆分
    result = {key:value for key,value in params.items() if key != 'stratety'} # 以这个为根基做一个新的
    # 这里需要取消一个键
    result['final_value'] = final_value
    result['sharpe'] = sharpe
    result['max_dd'] = max_dd
    result['code'] = _code
    #
    # logger.info(f'完成测试：最后金额:{final_value},{params}')
    return result



def wrapper(kwargs):
    return run_strategy(**kwargs)

def testStrategyByParams(stratety:bt.Strategy=None,code=None,**params):
    """用于调优，输出最最佳参数的

    Args:
        stratety (bt.Strategy): 交易策略
        code: 序号或者股票代码
    """
    # 将参数组成类似笛卡尔积的形式
    _keys = list(params.keys())
    _values = list(params.values())
    param_grid = [dict(zip(_keys, combo)) for combo in product(*_values)]
    # 然后每一项都要添加策略和股票代码
    for i in range(len(param_grid)):
        param_grid[i]['stratety'] = stratety
        param_grid[i]['code'] = code
    # 输出参数
    logger.info(f'参数组合数量:{len(param_grid)}')
    # 并行运行,用一半的cpu运行
    with Pool(processes=os.cpu_count()/2) as pool:
        results = pool.map(wrapper, param_grid)

    # 转换为 DataFrame 进行分析
    df = pd.DataFrame(results)
    # 这里根据最后的金额比较
    print(df.sort_values('final_value', ascending=False).head(20))
    
def testStrategyByParams2(stratety:bt.Strategy=None,**params):
    """测试所有的股票，查看最优参数的。

    Args:
        stratety (bt.Strategy, optional): _description_. Defaults to None.
    """
        # 将参数组成类似笛卡尔积的形式
    _keys = list(params.keys())
    _values = list(params.values())
    param_grid = [dict(zip(_keys, combo)) for combo in product(*_values)]
    # 然后每一项都要添加策略和股票代码
    for i in range(len(param_grid)):
        param_grid[i]['stratety'] = stratety
    # 输出参数
    logger.info(f'参数组合数量:{len(param_grid)}')
    best_result = []
    # 然后遍历所有的股票
    for i in range(len(codes)):
        _code = codes[i]
        # 这里需要将每项的
        for j in range(len(param_grid)):
            param_grid[j]['code'] = _code
        # 然后用多进程来做
        cpu_count = int(os.cpu_count()/2)
        with Pool(processes=cpu_count) as pool:
            results = pool.map(wrapper, param_grid)
        # 这里进行排序，取得最高的
        results.sort(key=lambda x:x['final_value'], reverse=True) # 降序
        best_result.append(results[0])
        logger.info(f'{i}/{len(codes)}:  result : {results[0]}')
    # 保存起来
    df = pd.DataFrame(best_result)
    return df
        


if __name__ == '__main__':
    pass