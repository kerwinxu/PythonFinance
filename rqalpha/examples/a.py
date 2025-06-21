#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-01-06 09:26:59
"""@File Name: a.py
@Author:  kerwin.cn@gmail.com
@Created Time:2018-01-06 09:26:35
@Last Change: 2018-01-06 09:26:35
@Description :
"""
# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    #沪深300指数、中证500指数和国债指数
    context.stocks = ["000300.XSHG","000905.XSHG","000012.XSHG"]
# before_trading此函数会在每天交易开始前被调用，当天只会被调用一次
# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑
    hs300 = history_bars(context.stocks[0],20,"1d","close")
    zz500 = history_bars(context.stocks[1],20,"1d","close")
    hsIncrease = hs300[19] - hs300[0]
    zzIncrease = zz500[19] - zz500[0]
    p = context.portfolio.positions
    hsQuality = p[context.stocks[0]].quantity
    zzQuality = p[context.stocks[1]].quantity
    gzQuality = p[context.stocks[2]].quantity
    if hsIncrease < 0 and zzIncrease < 0:
        if hsQuality > 0:
            order_target_percent(context.stocks[0],0)
            logger.info("卖出沪深300")
        if zzQuality > 0:
            order_target_percent(context.stocks[1],0)
            logger.info("卖出中证500")
        if gzQuality <= 0.001:
            order_target_percent(context.stocks[2],1)
            logger.info("买入国债")
    elif hsIncrease < zzIncrease:
        if hsQuality > 0:
            order_target_percent(context.stocks[0],0)
            logger.info("卖出沪深300")
        if gzQuality > 0:
            order_target_percent(context.stocks[2],0)
            logger.info("卖出国债")
        if zzQuality <= 0.001:
            order_target_percent(context.stocks[1],1)
            logger.info("买入中证500")
    else:
        if zzQuality > 0:
            order_target_percent(context.stocks[1],0)
            logger.info("卖出中证500")
        if gzQuality > 0:
            order_target_percent(context.stocks[2],0)
            logger.info("卖出国债")
        if hsQuality <= 0.01:
            order_target_percent(context.stocks[0],1)
            logger.info("买入沪深300")
