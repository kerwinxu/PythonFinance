#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2017-12-30 10:03:27
"""@File Name: AUTD_zip.py
@Author:  kerwin.cn@gmail.com
@Created Time:2017-12-29 21:27:51
@Last Change: 2017-12-29 21:27:51
@Description :  看看AUTD的zip转向
"""

import sys
import os
sys.path.append(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        "../../FinanceDataSource"))
import FinanceDataSource

from zip import get_zip
from zip import get_zip_ratio
from zip import get_zip_all

_data = FinanceDataSource.get_data(FinanceDataSource.str_tonghuashun,
                                   FinanceDataSource.tonghuashun_AUTD)

_lst = get_zip_all(_data, FinanceDataSource.str_close, 2)
print("get_zip_all(_data, FinanceDataSource.str_close, 2)")
print(_lst)
print(sum(_lst))
print(sum(_lst)/len(_lst))


_lst = get_zip_all(_data, FinanceDataSource.str_close, 1)
print("get_zip_all(_data, FinanceDataSource.str_close, 1)")
print(_lst)
print(sum(_lst))
print(sum(_lst)/len(_lst))
"""
得到如下结果：
get_zip_all(_data, FinanceDataSource.str_close, 2)
[-2.54, -0.8799999999999999, -0.4700000000000002, -1.19, 1.83, 1.7000000000000002, 5.890000000000001, 0.7000000000000002, -1.94, 1.3099999999999996, -0.3799999999999999, 2.1100000000000003, 0.54, -0.33999999999999986, 2.38, 2.2300000000000004, 1.4000000000000004]
12.350000000000001
0.7264705882352942
get_zip_all(_data, FinanceDataSource.str_close, 1)
[-0.54, 1.12, 0.08000000000000007, -0.78, 0.6699999999999999, 0.81, 0.06000000000000005, -0.6799999999999999, 3.0999999999999996, 3.7, 7.890000000000001, 2.7, 0.06000000000000005, 1.79, -0.77, 0.73, 1.62, 1.81, -0.98, 1.2599999999999998, 2.54, 0.75, -0.8500000000000001, 0.06000000000000005, 4.38, 3.8499999999999996, -0.8799999999999999, -0.51, 0.08000000000000007, -0.5900000000000001, -0.15999999999999992, -0.96, -0.1299999999999999, -0.7, 1.38, -0.42999999999999994]
31.479999999999993
0.8744444444444442
可以看到用这种方式不怎么划算，zip转向，本身是偏离到一定程度才确定最高点或最低点的
，是未来函数，实际操作的时候，这个偏离是要计算进去的。
虽说最后得到的是一个12%的增长，一个是31%的增长，但是，整个波段中，我放弃了2 * ratio的，最低2%的风险，来追求不到1%的利润，风险太高了吧。


"""
