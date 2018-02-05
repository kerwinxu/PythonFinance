#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-02-05 17:32:05
"""@File Name: tushare_data.py
@Author:  kerwin.cn@gmail.com
@Created Time:2018-02-04 10:59:51
@Last Change: 2018-02-04 10:59:51
@Description : 这个是将tushare的数据保存起来，以便我在本地调用的
通过网络不是十分方便，我在本地用HDF5来存储数据。
存储的数据主要是财务方面的数据，
    业绩报告（主表）
    盈利能力
    营运能力
    成长能力
    偿债能力
    现金流量
"""

import tushare as ts
import pandas as pd
import os
import time
import numpy as np
import datetime

str_report = 'report'       # 业绩报告总表
str_profit = 'profit'       # 盈利能力
str_operation = 'operation'     # 营运能力
str_growth = 'growth'           # 成长能力
str_debtpaying = 'debtpaying'   # 偿债能力
str_cashflow = 'cashflow'       # 现金流。
str_stock_basic = 'stock_basics'      # 股票的基本情况。

h5_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "tushare_data.h5")
stone = pd.HDFStore(h5_file_path, "a", complevel=9, complib='zlib')

dict_stock_basics = {
    'name': 'str',
    'industry': 'str',
    'area': 'str',
    'pe': 'float',
    'outstanding': 'float',
    'totals': 'float',
    'totalAssets': 'float',
    'liquidAssets': 'float',
    'fixedAssets': 'float',
    'reserved': 'float',
    'reservedPerShare': 'float',
    'esp': 'float',
    'bvps': 'float',
    'pb': 'float',
    'timeToMarket': 'float',
    'undp': 'float',
    'perundp': 'float',
    'rev': 'float',
    'profit': 'float',
    'gpr': 'float',
    'npr': 'float',
    'holders': 'float',
}

lst_report_column_name = ['code',
                          'year_quarter',
                          'name',
                          'eps',
                          'eps_yoy',
                          'bvps',
                          'roe',
                          'epcf',
                          'net_profits',
                          'profits_yoy',
                          'distrib',
                          'report_date',
                          ]
dict_report_columns = {
    'code': 'str',
    'year_quarter': 'str',
    'name': 'str',
    'eps': 'float',
    'eps_yoy': 'float',
    'bvps': 'float',
    'roe': 'float',
    'epcf': 'float',
    'net_profits': 'float',
    'profits_yoy': 'float',
    'distrib': 'str',
    'report_date': 'str'
}
lst_profit_column_name = ['code',
                          'year_quarter',
                          'name',
                          'roe',
                          'net_profit_ratio',
                          'gross_profit_rate',
                          'net_profits',
                          'eps',
                          'business_income',
                          'bips'
                          ]
dict_profit_columns = {
    'code': 'str',
    'year_quarter': 'str',
    'name': 'str',
    'roe': 'float',
    'net_profit_ratio': 'float',
    'gross_profit_rate': 'float',
    'net_profits': 'float',
    'eps': 'float',
    'business_income': 'float',
    'bips': 'float'
}

lst_operation_column_name = ['code',
                             'year_quarter',
                             'name',
                             'arturnover',
                             'arturndays',
                             'inventory_turnover',
                             'inventory_days',
                             'currentasset_turnover',
                             'currentasset_days']
dict_operation_column_ = {
    'code': 'str',
    'year_quarter': 'str',
    'name': 'str',
    'arturnover': 'float',
    'arturndays': 'float',
    'inventory_turnover': 'float',
    'inventory_days': 'float',
    'currentasset_turnover': 'float',
    'currentasset_days': 'float'}

lst_growth_column_name = ['code',
                          'year_quarter',
                          'name',
                          'mbrg',
                          'nprg',
                          'nav',
                          'targ',
                          'epsg',
                          'seg']

dict_growth_columns = {
    'code': 'str',
    'year_quarter': 'str',
    'name': 'str',
    'mbrg': 'float',
    'nprg': 'float',
    'nav': 'float',
    'targ': 'float',
    'epsg': 'float',
    'seg': 'float'
}

lst_debtpaying_column_name = ['code',
                              'year_quarter',
                              'name',
                              'currentratio',
                              'quickratio',
                              'cashratio',
                              'icratio',
                              'sheqratio',
                              'adratio']
dict_debtpaying_column = {
    'code': 'str',
    'year_quarter': 'str',
    'name': 'str',
    'currentratio': 'float',
    'quickratio': 'float',
    'cashratio': 'float',
    'icratio': 'float',
    'sheqratio': 'float',
    'adratio': 'float'
}

lst_cashflow_column_name = ['code',
                            'year_quarter',
                            'name',
                            'cf_sales',
                            'rateofreturn',
                            'cf_nm',
                            'cf_liabilities',
                            'cashflowratio']

dict_cashflow_column = {
    'code': 'str',
    'year_quarter': 'str',
    'name': 'str',
    'cf_sales': 'float',
    'rateofreturn': 'float',
    'cf_nm': 'float',
    'cf_liabilities': 'float',
    'cashflowratio': 'float',
}


def get_all_cashflow_data(year, quarter):
    year_quarter = "{}-{}".format(year, quarter)
    year_quarter_where = 'year_quarter=="{}"'.format(year_quarter)

    if((stone.get_storer(str_cashflow) is None) or
            (len(stone.select(str_cashflow, where=[year_quarter_where])) == 0)):
        pf = ts.get_cashflow_data(year, quarter)
        # 如果为空，就返回空吧
        if ((pf is None) or (len(pf) == 0)):
            return None
        # 添加月份，
        pf['year_quarter'] = year_quarter
        # 转换格式
        pf = pf.astype(dict_cashflow_column, copy=True, errors='ignore')
        # 保存数据到HDF5
        stone.append(str_cashflow, pf,
                     format='table',
                     data_columns=lst_cashflow_column_name
                     )
        # 返回这个值就可以了。
        return pf
    return stone.select(str_cashflow, where=[year_quarter_where])


def get_all_debtpaying_data(year, quarter):
    year_quarter = "{}-{}".format(year, quarter)
    year_quarter_where = 'year_quarter=="{}"'.format(year_quarter)

    if((stone.get_storer(str_debtpaying) is None) or
            (len(stone.select(str_debtpaying, where=[year_quarter_where])) == 0)):
        pf = ts.get_debtpaying_data(year, quarter)
        # 如果为空，就返回空吧
        if ((pf is None) or (len(pf) == 0)):
            return None
        # 添加月份，
        pf['year_quarter'] = year_quarter
        # 这个需要清洗数据
        pf = pf.replace('--', 0)
        # 转换格式
        pf = pf.astype(dict_debtpaying_column, copy=True, errors='ignore')
        # 保存数据到HDF5
        stone.append(str_debtpaying, pf,
                     format='table',
                     data_columns=lst_debtpaying_column_name
                     )
        # 返回这个值就可以了。
        return pf
    return stone.select(str_debtpaying, where=[year_quarter_where])


def get_all_growth_data(year, quarter):
    year_quarter = "{}-{}".format(year, quarter)
    year_quarter_where = 'year_quarter=="{}"'.format(year_quarter)

    if((stone.get_storer(str_growth) is None) or
            (len(stone.select(str_growth, where=[year_quarter_where])) == 0)):
        pf = ts.get_growth_data(year, quarter)
        # 如果为空，就返回空吧
        if ((pf is None) or (len(pf) == 0)):
            return None
        # 添加月份，
        pf['year_quarter'] = year_quarter
        # 转换格式
        pf = pf.astype(dict_growth_columns, copy=True, errors='ignore')
        # 保存数据到HDF5
        stone.append(str_growth, pf,
                     format='table',
                     data_columns=lst_growth_column_name
                     )
        # 返回这个值就可以了。
        return pf
    return stone.select(str_growth, where=[year_quarter_where])


def get_all_operation_data(year, quarter):
    year_quarter = "{}-{}".format(year, quarter)
    year_quarter_where = 'year_quarter=="{}"'.format(year_quarter)

    if((stone.get_storer(str_operation) is None) or
            (len(stone.select(str_operation, where=[year_quarter_where])) == 0)):
        pf = ts.get_operation_data(year, quarter)
        # 如果为空，就返回空吧
        if ((pf is None) or (len(pf) == 0)):
            return None
        # 添加月份，
        pf['year_quarter'] = year_quarter
        # 转换格式
        pf = pf.astype(dict_operation_column_, copy=True, errors='ignore')
        # 保存数据到HDF5
        stone.append(str_operation, pf,
                     format='table',
                     data_columns=lst_operation_column_name
                     )
        # 返回这个值就可以了。
        return pf
    return stone.select(str_operation, where=[year_quarter_where])


def get_all_profit_data(year, quarter):
    """
        Description : 取得盈利能力
        Arg :
            @year ： 年份
            @quarter ： 季度
        Returns : 返回DataFrame
        Raises	 :
    """
    year_quarter = "{}-{}".format(year, quarter)
    year_quarter_where = 'year_quarter=="{}"'.format(year_quarter)

    if((stone.get_storer(str_profit) is None) or
            (len(stone.select(str_profit, where=[year_quarter_where])) == 0)):
        pf = ts.get_profit_data(year, quarter)
        # 如果为空，就返回空吧
        if ((pf is None) or (len(pf) == 0)):
            return None
        # 添加月份，
        pf['year_quarter'] = year_quarter
        # 转换格式
        pf = pf.astype(dict_profit_columns, copy=True, errors='ignore')
        # 保存数据到HDF5
        stone.append(str_profit, pf,
                     format='table',
                     data_columns=lst_profit_column_name
                     )
        # 返回这个值就可以了。
        return pf
    return stone.select(str_profit, where=[year_quarter_where])


def get_all_report_data(year, quarter):
    """
        Description : 获得某年度季度的所有股票的业绩报告主表。
        Arg :
            @year ： 年份
            @quarter ： 季度
        Returns : 返回DataFrame
        Raises	 :
    """
    # 首先判断是否存在这个业绩报表, 不存在就新建
    #       新建业绩报表
    # 然后筛选年份季度，如果不存在就新建
    # 建立几个变量
    year_quarter = "{}-{}".format(year, quarter)

    # 如果没有这个报表或者包括为空，都新建了
    if ((stone.get_storer(str_report) is None) or
            (len(stone.select(str_report, where=['year_quarter=="{}"'.format(year_quarter)])) == 0)):
        # 下载报告
        pf = ts.get_report_data(year, quarter)
        # 如果为空，就返回空吧
        if ((pf is None) or (len(pf) == 0)):
            return None
        # 添加月份，
        pf['year_quarter'] = year_quarter
        # 转换格式
        pf = pf.astype(dict_report_columns, copy=True, errors='ignore')
        # 保存数据到HDF5
        stone.append(str_report, pf,
                     format='table',
                     min_itemsize={
                         'distrib': 50},
                     data_columns=lst_report_column_name
                     )
        # 返回这个值就可以了。
        return pf

    return stone.select(str_report, where=[
        'year_quarter=="{}"'.format(year_quarter)])

    # 如下的是原先的实现，也是可以运行的。
    if stone.get_storer(str_report) is None:
        # 下载报告
        pf = ts.get_report_data(year, quarter)
        # 添加月份，
        pf['year_quarter'] = year_quarter
        # 保存数据到HDF5
        stone.append(str_report, pf,
                     format='table',
                     min_itemsize={
                         'distrib': 20},
                     data_columns=lst_report_column_name
                     )
        # 返回这个值就可以了。
        return pf

    pf2 = stone.select(str_report, where=[
        'year_quarter=="{}"'.format(year_quarter)])
    if len(pf2) == 0:
        # 下载报告
        pf = ts.get_report_data(year, quarter)
        # 添加月份，
        pf['year_quarter'] = year_quarter
        # 跟原先的合并
        stone.append(str_report, pf)
        return pf
    return pf2


def get_all_finance_data(finance_type, code):
    """
        Description : 取得某公司所有的财务数据。
        Arg :
            @finance_type : 财务数据的类别
            @code : 股票代码。
        Returns :
        Raises	 :
    """
    code_where = 'code=="{}"'.format(get_tushare_code(code))
    return stone.select(finance_type, where=[code_where])


def get_tushare_code(code):
    """
        Description : 取得tushare接受的code数据。
        Arg :
        Returns :
        Raises	 :
    """
    # 主要是rqalpha的股票代码表示是"000300.XSHG",
    # 而tushare需要的仅仅是000300
    if len(code) == 6:
        return code
    # 其他的先做省事吧。
    return code[:6]
    pass


def get_finance_data(finance_type, code, year, quarter):
    """
        Description : 取得某公司某季度的财务数据
        Arg :
            @finance_type : 财务数据类别
            @code: 股票代码
            @year ：年份
            @quarter : 季度
        Returns :
        Raises	 :
    """
    code_where = 'code=="{}"'.format(get_tushare_code(code))
    year_quarter = "{}-{}".format(year, quarter)
    year_quarter_where = 'year_quarter=="{}"'.format(year_quarter)
    return stone.select(finance_type, where=[code_where, year_quarter_where])


def get_stock_basics(code):
    """
        Description : 取得某个股票的基本信息，请注意这个只是取得最近的基本信息。
        不能设定时间的。
        Arg :
        Returns :
        Raises	 :
    """
    code_where = 'index=="{}"'.format(get_tushare_code(code))
    return stone.select(str_stock_basic, where=[code_where])

    pass


def init_stock_basics():
    """
        Description : 初始化上市公司的基本情况的。
        Arg :
        Returns :
        Raises	 :
    """
    pf = ts.get_stock_basics()
    pf = pf.astype(dict_stock_basics, copy=True, errors='ignore')
    stone.put(str_stock_basic, pf,
              format='table',
              data_columns=dict_stock_basics)


def init_data():
    """
        Description : 数据的初始化。
        Arg :
        Returns :
        Raises	 :
    """
    init_stock_basics()
    start_year = 1990
    end_year = int(datetime.datetime.now().strftime("%Y")) + 1
    for year in range(start_year, end_year):
        for quarter in range(1, 5):
            print("{} - {}".format(year, quarter))
            list_fun = [
                get_all_debtpaying_data,
                get_all_cashflow_data,
                # get_all_growth_data,
                get_all_operation_data,
                get_all_profit_data,
                get_all_report_data]
            for _fun in list_fun:
                time.sleep(10)
                print("run: {}".format(_fun.__name__))
                _fun(year, quarter)


if __name__ == '__main__':
    print(get_stock_basics('000002'))
    # init_stock_basics()
    # init_data()
    # print(get_all_finance_data(str_report, '000001'))
    # print(get_finance_data(str_report, '300419', 2014, 3))
    pass
