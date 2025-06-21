#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-01-06 22:02:49
"""@File Name: Bcolz_macd.py
@Author:  kerwin.cn@gmail.com
@Created Time:2018-01-06 20:49:05
@Last Change: 2018-01-06 20:49:05
@Description :
"""

from iBcolz import iBcolz

class Bcolz_macd(iBcolz):
    def __init__(self):
        super().__init__()

    def add_indicator(self):
        pass

_b = Bcolz_macd()
_b.add_indicator()
print(_b)
_b.flush()
