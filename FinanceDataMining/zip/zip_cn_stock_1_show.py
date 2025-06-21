#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-01-17 21:18:32
"""@File Name: zip_cn_stock_1_show.py
@Author:  kerwin.cn@gmail.com
@Created Time:2018-01-15 23:37:37
@Last Change: 2018-01-15 23:37:37
@Description : 这个只是另一个的显示
"""

import os
import shelve
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


if __name__ == '__main__':
    #   读取数据
    _file_name = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        "zip_cn_stock_1_sheve")
    _file = shelve.open(_file_name)
    _up = _file['up']
    _down = _file['down']
    _file.close()
    print("导入数据完毕")

    _up_2 = [round(_i, 0) for _i in _up]
    _up_2 = np.array(_up_2)
    _down_2 = [round(_i, 0) for _i in _down]
    _down_2 = np.array(_down_2)
    # 显示
    # sns.distplot(_up_2, rug=True, hist=True)
    # plt.show()
    print("高点的")
    print("所有的数量：{}".format(len(_up_2)))
    print("小于0%的数量：{}".format(len(_up_2[_up_2 < 0])))
    print("大于10%的数量：{}".format(len(_up_2[_up_2 > 10])))
    print("大于20%的数量：{}".format(len(_up_2[_up_2 > 20])))
    print("大于30%的数量：{}".format(len(_up_2[_up_2 > 30])))
    print("大于40%的数量：{}".format(len(_up_2[_up_2 > 40])))
    print("大于50%的数量：{}".format(len(_up_2[_up_2 > 50])))
    print("大于60%的数量：{}".format(len(_up_2[_up_2 > 60])))
    print("大于70%的数量：{}".format(len(_up_2[_up_2 > 70])))
    print("大于80%的数量：{}".format(len(_up_2[_up_2 > 80])))
    print("大于90%的数量：{}".format(len(_up_2[_up_2 > 90])))
    print("大于100%的数量：{}".format(len(_up_2[_up_2 > 100])))
    print("大于100%的数量：{}".format(len(_up_2[_up_2 > 100])))
    print("大于200%的数量：{}".format(len(_up_2[_up_2 > 200])))
    print("大于300%的数量：{}".format(len(_up_2[_up_2 > 300])))

    print("低点的")
    print("所有的数量：{}".format(len(_down_2)))
    print("高于5%的数量：{}".format(len(_down_2[_down_2 > 5])))
    print("高于0%的数量：{}".format(len(_down_2[_down_2 > 0])))
    print("跌于0%的数量：{}".format(len(_down_2[_down_2 < 0])))
    print("跌于5%的数量：{}".format(len(_down_2[_down_2 < -5])))
    print("跌于10%的数量：{}".format(len(_down_2[_down_2 < -10])))

    # 我筛选，最低点也是高于0%的
    print("最低点大于5%，然后查看最高点的")
    _up_3 = _up_2[_down_2 > 5]
    print("中位数：{}".format(np.median(_up_3)))
    print("平均值：{}".format(_up_3.mean()))
    print("最小值：{}".format(_up_3.min()))
    # sns.distplot(_up_3, rug=True, hist=True)
    # plt.show()
