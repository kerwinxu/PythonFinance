#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2017-12-30 10:03:33
"""@File Name: AUTD_up_down.py
@Author:  kerwin.cn@gmail.com
@Created Time:2017-12-28 20:58:42
@Last Change: 2017-12-28 20:58:42
@Description :  这个是取得zip转向数据的。
"""

import sys
import os
sys.path.append(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        "../../FinanceDataSource"))
import FinanceDataSource

def get_zip(dataframe, k=FinanceDataSource.str_close, ratio=2):
    """
        Description : 取得zip转向的列表
        Arg :
            @dataframe : 数据 ，frame
            @k : 是收盘价，开盘价，最高价，最低价
            @ratio : 判断转向的比率
        Returns : 取得zip转向的波峰波谷值的列表
        Raises	 :
            @IndexError : 只支持开盘价，收盘价之类的

    """
    # 判断是否是支持的k
    if k not in [FinanceDataSource.str_close,
                 FinanceDataSource.str_open,
                 FinanceDataSource.str_high,
                 FinanceDataSource.str_low]:
        # 发出异常
        raise IndexError('只支持开盘价、收盘价、最高价和最低价, 暂不支持：' +str(k))
    # 这个是记录最高点和最低点的
    lst_zip = []
    # 这个是一个状态，是否是上涨的
    is_up = False
    # 根据用户选择，看看是判断收盘价还是开盘价等等
    lst_k = list(dataframe[k])
    # 添加第一项，
    lst_zip.append(lst_k[0])
    # 添加第二项
    lst_zip.append(lst_k[1])
    # 判断上涨还是下跌
    if(lst_k[1] > lst_k[0]):
        is_up = True
    # 如下是迭代数据, 从第三项开始。
    for i in lst_k[2:]:
        # 如果上涨
        if is_up:
            # 判断是否突破
            if i > lst_zip[-1]:
                # 就更新数据
                lst_zip[-1] = i
            elif lst_zip[-1] - i > lst_zip[-1] * (ratio / 100):
                # 如果转折了, 就添加新的一项
                lst_zip.append(i)
                is_up = False
        else:
            # 判断是否突破
            if i < lst_zip[-1]:
                # 更新数据
                lst_zip[-1] = i
            elif i - lst_zip[-1] > lst_zip[-1] * (ratio / 100):
                lst_zip.append(i)
                is_up = True
    # 返回
    return lst_zip

def get_zip_ratio(lst):
    """
        Description : 取得zip转向中波峰波谷的比值
        Arg :
        Returns :
        Raises	 :
    """
    lst_ratio = []
    for i in range(0, len(lst)-1):
        lst_ratio.append(round(((lst[i+1]-lst[i])/lst[i]*100), 2))
    return lst_ratio

def get_zip_result(lst, ratio):
    """
        Description : 根据得到的波谷比率，计算是否有可能根据这个来获利
                    比如在波峰损失一个ratio，而波谷又损失一个ratio，看看余下多少。
        Arg :
        Returns :
        Raises	 :
    """
    lst_won = []
    for i in range(len(lst)):
        if lst[i] > 0:
            lst_won.append(lst[i]-2*ratio)
        else:
            lst_won.append((0 - (lst[i] + 2 * ratio)))
    return lst_won

def get_zip_all(dataframe, k=FinanceDataSource.str_close, ratio=2):
    """
        Description : 这个是如上几个函数的综合
        Arg :
        Returns :
        Raises	 :
    """
    _lst = get_zip(dataframe, k, ratio)
    _lst = get_zip_ratio?!?jedi=0, (_lst)?!? (lst, *_*ratio*_*) ?!?jedi?!?
    _lst = get_zip_result(_lst, ratio)
    return _lst
