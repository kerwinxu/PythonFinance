#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-02-05 16:46:24
"""@File Name: MACD1.py
@Author:  kerwin.cn@gmail.com
@Created Time:2018-01-10 21:18:00
@Last Change: 2018-01-10 21:18:00
@Description : 这个是用macd为主做的交易系统。
    买入条件 ： macd金叉，这两天成交量疯涨。
    卖出条件 ： 5日均线下跌。
    注意 ： 我这里仅仅指示买卖一手。
"""
from rqalpha import run_func
from rqalpha.api import update_universe  # 更新股票池，这个是覆盖操作。
# 如下是下单相关
# 我这里主要用通用的
from rqalpha.api import submit_order # rqalpha.api.submit_order(id_or_ins, amount, side, price=None, position_effect=None)
from rqalpha.api import order   # 智能下单，单位手 rqalpha.api.order(order_book_id, quantity, price=None, style=None)
from rqalpha.api import order_to    # 智能下单，调仓到某个仓位，单位手 rqalpha.api.order_to(order_book_id, quantity, price=None, style=None)
from rqalpha.api import order_percent # 发送一个花费价值等于目前投资组合（市场价值和目前现金的总和）一定百分比现金的买/卖单，正数代表买，负数代表卖rqalpha.api.order_percent(id_or_ins, percent, price=None, style=None)
# 持仓查询接口
from rqalpha.api import get_position # 获取某个标的的持仓对象 rqalpha.api.get_position(order_book_id, direction=POSITION_DIRECTION.LONG)
from rqalpha.api import get_positions  # 获取所有持仓对象列表
# 查询相关
from rqalpha.api import all_instruments  # 所有合约基础信息
from rqalpha.api import instruments     # 合约详细信息

from rqalpha.api import history_bars    # 某一个合约的历史数据，指定数量 rqalpha.api.history_bars(order_book_id, bar_count, frequency, fields=None, skip_suspended=True, include_now=False, adjust_type='pre')

# 这两个导入不了。
# from rqalpha.api import industry         # 行业股票列表
# from rqalpha.api import sector          # 板块股票列表
# from rqalpha.api import is_st_stock   #  ST股判断
# from rqalpha.api import is_suspended  # 全天停牌判断

# 撤单
from rqalpha.api import cancel_order    # 撤单
from rqalpha.api import get_open_orders  # 获得未成交订单数据

# from rqalpha.api import get_bars_all    # 某一个合约的历史数据，所有数量
# from rqalpha.api import get_future_contracts    # 期货可交易合约列表
# 交易日
from rqalpha.api import get_trading_dates   # 交易日列表
from rqalpha.api import get_previous_trading_date   # 上个交易日
from rqalpha.api import get_next_trading_date       # 下一个交易日
# 收益率
from rqalpha.api import get_yield_curve     # 获得国债收益率曲线
\
# 订阅
from rqalpha.api import subscribe        # 订阅合约行情，
from rqalpha.api import unsubscribe      # 取消订阅合约行情
from rqalpha.api import update_universe  # 更新合约池
# 添加指标
# from rqalpha.api import add_indicator   # 添加指标
# logger
from rqalpha.api import logger

# 定时器,只能在init内使用。
# from scheduler import run_daily, run_weekly, run_monthly, time_rule 

import datetime
import talib
import sys
import os


def is_predate_listed_date(book_id, days):
    """
        Description : 判断某个股票上市日期是否大于多少天
        Arg :
            @book_id : 股票ID
            @days : 天数
        Returns :
        Raises	 :
    """
    _instrument = instruments(book_id)
    _listed_date = _instrument.listed_date
    return (datetime.datetime.now() - _listed_date).days > days


def init(context):
    """
        Description : 程序初始化
        Arg :
        Returns :
        Raises	 :
    """
    # 这里设置参数
    context.TIME_PERIOD = 5
    # 获得所有股票，
    context.stocks = list(all_instruments('CS')['order_book_id'])
    # 删除ST股票, 不对ST股票做回测。
    # 上市90天的股票不做回测，因为前几天都是疯涨。然后暴跌。
    context.stocks = [
        _stock for _stock in context.stocks
        if is_predate_listed_date(_stock, 90)]
        
    # 设置进入股票池
    update_universe(context.stocks)

    # 使用MACD需要设置长短均线和macd平均线的参数
    context.SHORTPERIOD = 12
    context.LONGPERIOD = 26
    context.SMOOTHPERIOD = 9
    context.OBSERVATION = 50
    # 成交将
    context.VOLUME_ZOOM = 2 


def before_trading(context):
    """
        Description : 每天交易策略开始前被调用。
        Arg :
        Returns :
        Raises	 :
    """
    pass


def handle_bar(context, bar_dict):
    """
        Description : 选择的证券的数据更新将会触发此段逻辑
        Arg :
        Returns :
        Raises	 :
    """
    # prices = history_bars("000001.XSHE", 6, '1d', 'close')
    # _ma5 = talib.SMA(prices, 5)
    # logger.info(_ma5[-1])
    # 我这里先看看有没有需要买入或者卖出的，然后再调整
    _buys = [] # 需要买入的
    _sells = [] # 需要卖出的
    for stock in context.stocks:
        # 遍历每一个股票
        prices = history_bars(stock, context.OBSERVATION, '1d', ['datetime', 'open','high', 'low', 'close','volume'])
        # 用Talib计算MACD取值，得到三个时间序列数组，分别为macd, signal 和 hist
        macd, signal, hist = talib.MACD(prices['close'], context.SHORTPERIOD,
                                    context.LONGPERIOD, context.SMOOTHPERIOD)
        # 这里判断是否存在金叉，且成交量足够大。
        if macd[-1] - signal[-1] > 0 and macd[-2] - signal[-2] < 0 \
            and (prices['volume'][-1] / prices['volume'][-2] >= context.VOLUME_ZOOM or prices['volume'][-2] / prices['volume'][-3] >= context.VOLUME_ZOOM):
            _buys.append(stock)
        
        # 这里判断5日均线是否
        _avg = talib.SMA(prices['close'], 5)
        if len(_avg) >= 3 and  _avg[-1] < _avg[-2] and _avg[-2] > _avg[-3]:
            _sells.append(stock)
    # print("买入:{}".format(_buys))
    # print("卖出:{}".format(_sells))
    # 这里进行调仓
    # 这里看看持仓
    _positions = [i.order_book_id for i in get_positions()]
    for stock in _sells:
        if stock in _positions:
            order_to(stock, 0)
    for stock in _buys:
        order_to(stock , 100)
    


def after_trading(context):
    """
        Description : 每天交易结束后调用。
        Arg :
        Returns :
        Raises	 :
    """
    pass


config = {
    "base": {
        "start_date": (datetime.datetime.now()- datetime.timedelta(days=365*1)).strftime("%Y-%m-%d"),
        "end_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "frequency": "1d",
        "matching_type": "current_bar",
        "benchmark": "000300.XSHG",
        "accounts": {
            "stock": 1000000
        }
    },
    "extra": {
        "log_level": "verbose",
    },
    "mod": {
        "sys_analyser": {
            "enabled": True,
            "plot": True
        },
        "sys_progress":{
            # 是否在命令行/终端绘制进度条
            "show": True,
        }
    }
}


# 如下是运行回测。
starttime = datetime.datetime.now()
# 您可以指定您要传递的参数
run_func(
    init=init,
    before_trading=before_trading,
    handle_bar=handle_bar,
    after_trading=after_trading,
    config=config)

endtime = datetime.datetime.now()
print("程序运行时间：" + str((endtime - starttime).seconds) + "秒")
