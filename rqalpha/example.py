#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-01-17 09:59:36
"""@File Name: example.py
@Author:  kerwin.cn@gmail.com
@Created Time:2018-01-10 21:18:00
@Last Change: 2018-01-10 21:18:00
@Description :
"""
from rqalpha import run_func
from rqalpha.api import update_universe # 更新股票池，这个是覆盖操作。
# 如下是下单相关
# 股票期货通用
from rqalpha.api import order   # 智能下单，单位手
from rqalpha.api import order_to    # 智能下单，调仓到某个仓位，单位手
# 股票专用
from rqalpha.api import order_value # 指定价值交易，股票专用
from rqalpha.api import order_percent   # 一定比例下单，股票专用，发送一个等于目前投资组合价值（市场价值和目前现金的总和）一定百分比的买/卖单，
from rqalpha.api import order_target_value  # 指定目标价值下单，股票专用。
from rqalpha.api import order_target_percent    # 目标比例下单，指定投资组合的目标百分比，股票专用
# 期货专用
from rqalpha.api import buy_open    # 买入开仓
from rqalpha.api import buy_close   # 买入平仓
from rqalpha.api import sell_open   # 卖出开仓
from rqalpha.api import sell_close  # 卖出平仓
# 撤单
from rqalpha.api import cancel_order    # 撤单
from rqalpha.api import get_open_orders # 获得未成交订单数据
# 查询相关
from rqalpha.api import all_instruments # 所有合约基础信息
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
from rqalpha.api import is_st_stock # 是否是ST股票
# 订阅
from rqalpha.api import subscribe   # 订阅合约行情，
from rqalpha.api import unsubscribe # 取消订阅合约行情
# 添加指标
from rqalpha.api import add_indicator   # 添加指标
# logger
from rqalpha.api import logger

import datetime
import talib
import sys, os
sys.path.append(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        "../FinanceDataSource"))
import  FinanceDataSource


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
        _ma_5 = talib.SMA(_close, context.TIME_PERIOD)
        # 将指标数据保存
        add_indicator(_book_id, '1d', "ma_5", _ma_5)
        #
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
    _ma_5 = history_bars("000001.XSHE", 1, '1d', 'ma_5')
    logger.info(_ma_5)
    pass


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


# 如下是运行回测。
starttime = datetime.datetime.now()
# 您可以指定您要传递的参数
run_func(
        init=init,
        before_trading=before_trading,
        handle_bar=handle_bar,
        config=config)

endtime = datetime.datetime.now()
print("程序运行时间：" + str((endtime - starttime).seconds))
