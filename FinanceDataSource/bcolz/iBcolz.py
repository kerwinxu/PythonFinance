#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-01-06 21:08:01
"""@File Name: iBcolz.py
@Author:  kerwin.cn@gmail.com
@Created Time:2018-01-06 20:26:31
@Last Change: 2018-01-06 20:26:31
@Description :
"""

import bcolz

class iBcolz:
    """
    Attributes	:
    functions	:

    """
    _rqalpha_rootdir = r"E:\home\kerwin\.rqalpha\bundle\stocks.bcolz"

    def __init__(self, _dir=None):
        if _dir is None:
            _dir =self._rqalpha_rootdir
        self.f_bcolz = bcolz.open(rootdir=_dir, mode='a')

    def flush(self):
        """
            Description : 将数据刷新到磁盘
            Arg :
            Returns :
            Raises	 :
        """
        self.f_bcolz.flush()

    def add_indicator(self):
        """
            Description : 添加指标
            Arg :
            Returns :
            Raises	 :
        """
        pass
