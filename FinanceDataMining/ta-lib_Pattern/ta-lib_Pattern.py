#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-06 23:05:12
# Last Change:  2018-02-05 14:02:08
# File Name: adaptive_ma_1.py
# 这个是运用Ta-lib中的模式识别来判断。

import sys
sys.path.append("../FinanceDataSource")
import FinanceDataSource
import numpy as np
import talib

def get_tonghuashun_AGUSDO_data():
    """取得同花顺上的白银数据"""
    return FinanceDataSource.get_tonghuashun_data(FinanceDataSource.tonghuashun_AGUSDO)


def pattern(cdl_fun, data):
    """参数只有一个，就是talib的CDL簇函数"""
    print("模式：%s" % (cdl_fun))
    open_data = data['Open'].as_matrix()
    high_data = data['High'].as_matrix()
    low_data = data['Low'].as_matrix()
    close_data = data['Close'].as_matrix()
    # 取得模式识别
    cdl = eval(cdl_fun + "(open_data, high_data, low_data, close_data)")
    bool_cdl = cdl == 100
    # 在开头插入1天。
    bool_cdl = np.insert(bool_cdl, 0, False)
    # 删去最后一天的。
    bool_cdl = bool_cdl[:len(bool_cdl) - 1]
    # 打印日期
    print(data[bool_cdl].index)
    diff_close_open = (close_data - open_data)[bool_cdl]
    summary(diff_close_open)
    print("*********************************************************")

    pass


def summary(_lst):
    """这个是摘要"""
    if(len(_lst) == 0):
        return
    summary2(_lst)
    arr_temp = np.array(_lst)
    print("up")
    arr_up = arr_temp[arr_temp > 0]
    summary2(arr_up)
    print("down")
    arr_down = arr_temp[arr_temp < 0]
    summary2(arr_down)


def summary2(arr):
    if(len(arr) == 0):
        return
    print("len %d" % len(arr))
    print("最小：%f" % np.min(arr))
    print("均值：%f" % np.mean(arr))
    print("中位数：%f" % np.median(arr))
    print("最大值：%f" % np.max(arr))


if __name__ == "__main__":
    silver_data = get_tonghuashun_AGUSDO_data()
    # 用dir来取得所有的属性方法
    for i in dir(talib):
        # 判断开始是不是“CDL”
        if(i[:3] == "CDL"):
            s = "talib." + i
            pattern(s, silver_data)
#   pattern(talib.CDL2CROWS, silver_data)
