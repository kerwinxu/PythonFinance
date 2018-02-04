#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-01-29 15:31:22
"""@File Name: example.py
@Author:  kerwin.cn@gmail.com
@Created Time:2018-01-10 21:18:00
@Last Change: 2018-01-10 21:18:00
@Description :
交易策略
仅仅运用多头趋势回撤的思路，我们构建策略如下：

一、选定一股票池，并且选定一系列系数：
二、一组均线天数 [N1,N2,N3,…,Nk][N1,N2,N3,…,Nk]：总数量 kk 限制，按照从小到大 N1≤N2≤⋯≤NkN1≤N2≤⋯≤Nk 排列。当相应天数的移动均线是从大到小排列时，是多头排列的格局；
三、趋势天数 TT： 当上面指定的移动均线在 TT 天内都处于多头排列时，我们才判断价格处于多头趋势；
四、回撤均线 MM：当前一天的最收盘价低于 MM 日均线时时判断为回撤；
五、持有股票上限 num_stocks：同时最多持仓 num_stocks 支股票。
六、止损比例 dd 和止盈比例 uu：当股票价格搞出买入价的 uu 倍，或低于买入价的 dd 倍时，卖出股票。

每日执行以下操作
产生信号：
一、选出股票池中所有在过去的 TT 个交易日内，[N1,N2,N3,…,Nk][N1,N2,N3,…,Nk] 日均线组按照多头排列的股票，判定为多头趋势；
二、在处于多头趋势的股票中选出前一日收盘价低于 MM 日均线的股票，判定为发生回撤点；
三、在所有出现多头趋势回撤点的股票中，去掉已持仓的股票，其余的发出买入信号。
调换仓位：
一、全仓卖出所有达到止盈或止损线的股票；
二、在有现金的情况下，买入所有发出信号的股票，每支股票的买入总值为总资产净值除以 num_stocks。
    
"""
from rqalpha import run_func
from rqalpha.api import update_universe  # 更新股票池，这个是覆盖操作。
# 如下是下单相关
# 股票期货通用
from rqalpha.api import order   # 智能下单，单位手
from rqalpha.api import order_to    # 智能下单，调仓到某个仓位，单位手
# 股票专用
from rqalpha.api import order_value  # 指定价值交易，股票专用
# 一定比例下单，股票专用，发送一个等于目前投资组合价值（市场价值和目前现金的总和）一定百分比的买/卖单，
from rqalpha.api import order_percent
from rqalpha.api import order_target_value  # 指定目标价值下单，股票专用。
from rqalpha.api import order_target_percent    # 目标比例下单，指定投资组合的目标百分比，股票专用
# 期货专用
from rqalpha.api import buy_open    # 买入开仓
from rqalpha.api import buy_close   # 买入平仓
from rqalpha.api import sell_open   # 卖出开仓
from rqalpha.api import sell_close  # 卖出平仓
# 撤单
from rqalpha.api import cancel_order    # 撤单
from rqalpha.api import get_open_orders  # 获得未成交订单数据
# 查询相关
from rqalpha.api import all_instruments  # 所有合约基础信息
from rqalpha.api import instruments     # 合约详细信息
from rqalpha.api import industry        # 行业股票列表
from rqalpha.api import sector          # 板块股票列表
from rqalpha.api import history_bars    # 某一个合约的历史数据，指定数量
from rqalpha.api import get_bars_all    # 某一个合约的历史数据，所有数量
from rqalpha.api import get_future_contracts    # 期货可交易合约列表
# 交易日
from rqalpha.api import get_trading_dates   # 交易日列表
from rqalpha.api import get_previous_trading_date   # 上个交易日
from rqalpha.api import get_next_trading_date       # 下一个交易日
# 收益率
from rqalpha.api import get_yield_curve     # 获得国债收益率曲线
# ST股票
from rqalpha.api import is_st_stock  # 是否是ST股票
# 订阅
from rqalpha.api import subscribe   # 订阅合约行情，
from rqalpha.api import unsubscribe  # 取消订阅合约行情
# 添加指标
from rqalpha.api import add_indicator   # 添加指标
# logger
from rqalpha.api import logger

import datetime
import talib
import sys
import os
sys.path.append(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        "../FinanceDataSource"))
import FinanceDataSource


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
    context.LST_MA = [5, 10, 20, 60]   # 均线。
    context.LST_DUOTOU = []     # 保存的是均线持续多头的列表。
    context.DUOTOU_DAYS = 7      # 均线排列持续天数判断为多头趋势
    context.BACK_MA = 10        # 回测均线
    context.NUM_STOCKS = 10      # 最多持有股票数量
    context.STOP_PERCENT = 10   # 止损比例

    # 获得所有股票，
    _all_cn_stock = list(all_instruments('CS')['order_book_id'])
    # 删除ST股票, 不对ST股票做回测。
    # 上市90天的股票不做回测，因为前几天都是疯涨。然后暴跌。
    _all_cn_stock = [
        _stock for _stock in _all_cn_stock
        if not is_st_stock(_stock, 1)
        and is_predate_listed_date(_stock, 90)]

    for _book_id in _all_cn_stock:
        # 在这里添加指标的相关数据
        # 如下先取得K线数据
        _close = get_bars_all(_book_id, '1d', "close")
        _open = get_bars_all(_book_id, '1d', "open")
        _high = get_bars_all(_book_id, '1d', "high")
        _low = get_bars_all(_book_id, '1d', "low")
        _limit_down = get_bars_all(_book_id, '1d', "limit_down")
        _limit_up = get_bars_all(_book_id, '1d', "limit_up")
        _total_turnover = get_bars_all(_book_id, '1d', "total_turnover")
        _volume = get_bars_all(_book_id, '1d', "volume")
        # 计算指标
        # _ma_5 = talib.SMA(_close, context.TIME_PERIOD)
        # 将所有的均线保存在这个数组中。
        _lst_ma = []
        for _ma in context.LST_MA:
            _lst_ma.append(talib.SMA(_close, _ma))
        # 然后取得一个逻辑数组，是判断是否是均线多头的。
        _bool_up = []
        for _i in range(len(_lst_ma) - 1):
            # 每个都跟后边的比较一下。
            _bool_up = _bool_up and (_lst_ma[_i + 1] > _lst_ma[_i])
        # 将指标数据保存
        add_indicator(_book_id, '1d', "duotou", _bool_up)
        # 然后有个变量看看是否回撤的
        _ma_huiche = talib.SMA(_close, context.BACK_MA)
        _huiche = _close < _ma_huiche
        # 保存这个回撤的
        add_indicator(_book_id, '1d', "huiche", _huiche)
    # 设置进入股票池
    update_universe(_all_cn_stock)
    pass


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
    pass


def after_trading(context):
    """
        Arg :
        Returns :
        Raises	 :
    """
    pass


config = {
    "base": {
        "frequency": "1d",
        "matching_type": "current_bar",
        "benchmark": "000300.XSHG",
        "accounts": {
            "stock": 10000
        }
    },
    "extra": {
        "log_level": "verbose",
    },
    "mod": {
        "sys_analyser": {
            "enabled": True,
            "plot": True
        }
    }
}


def my_run():
    run_func(
        init=init,
        before_trading=before_trading,
        handle_bar=handle_bar,
        config=config)


# 您可以指定您要传递的参数

my_run()
