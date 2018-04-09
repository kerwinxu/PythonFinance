#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Change:  2018-02-07 21:19:38
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
            主要是rqalpha的股票代码表示是"000300.XSHG",
            而tushare需要的仅仅是000300
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


def get_quarter(_datetime):
    """
        Description : 根据日期返回年份季度
        Arg :
        Returns : (年份, 季度)
        Raises	 :
    """
    if (not isinstance(_datetime, datetime.datetime)):
        return None
    str_month = _datetime.strftime('%m')
    str_year = _datetime.strftime("%Y")
    if str_month in ['01', '02', '03']:
        return (str_year, '1')
    elif str_month in ['04', '05', '06']:
        return (str_year, '2')
    elif str_month in ['07', '08', '09']:
        return (str_year, '3')
    elif str_month in ['10', '11', '12']:
        return (str_year, '4')


def get_quarter_pre(_datetime):
    """
        Description : 取得某日期的上一个月份季度。
        Arg :
        Returns :
        Raises	 :
    """
    year, quarter = get_quarter(_datetime)
    if year is None:
        return None
    if quarter == '1':
        # 上一年啦。
        return str(int(year) - 1), '4'
    else:
        return year, str(int(quarter) - 1)


def get_last_finance_data_2(finance_type, lst_code, dt=None, n=4):
    """
        Description : 取得一些股票最近几个季度的财务数据
        Arg :
            @finance_type : 财务数据类别
            @lst_code   : 股票代码
            @dt     : 日期
            @n      : 取得的财务报表数量。
        Returns :
        Raises	 :
    """
    if dt is None:
        dt = datetime.datetime.now()
    if (not isinstance(dt, datetime.datetime)):
        raise NameError('dt参数类型必须是datetime类型')
    lst_code_where = []
    for _code in lst_code:
        lst_code_where.append('(code=="{}")'.format(get_tushare_code(_code)))
    code_where = ' | '.join(lst_code_where)
    _df = stone.select(finance_type, where=code_where)
    # 这时候就得判断日期了。
    # 取得某个日期的上一个季度的年份季度
    year, quarter = get_quarter_pre(dt)
    year_quarter = "{}-{}".format(year, quarter)
    # 运算季度减法
    _df['_quarter_sub'] = quarter_sub_func(_df['year_quarter'], year_quarter)
    # 然后筛选啦
    return _df.loc[((_df['_quarter_sub'] < 1) & (_df['_quarter_sub'] >= (0 - n)))]


def get_last_finance_data(finance_type, code, dt=None, n=4):
    """
        Description : 取得某个日期前面的n个财务数据
        Arg :
            @finance_type : 财务数据类别
            @code   : 股票代码
            @dt     : 日期
            @n      : 取得的财务报表数量。
        Returns :
        Raises	 :
            @ dt不是datetime类型。
    """
    if dt is None:
        dt = datetime.datetime.now()
    if (not isinstance(dt, datetime.datetime)):
        raise NameError('dt参数类型必须是datetime类型')
    # 股票代码改成tushare能接受的格式。
    code = get_tushare_code(code)
    # 组建查询字符串
    code_where = 'code=="{}"'.format(get_tushare_code(code))
    # 查询。
    _df = stone.select(finance_type, where=[code_where])
    # 这时候就得判断日期了。
    # 取得某个日期的上一个季度的年份季度
    year, quarter = get_quarter_pre(dt)
    year_quarter = "{}-{}".format(year, quarter)
    # 运算季度减法
    _df['_quarter_sub'] = quarter_sub_func(_df['year_quarter'], year_quarter)
    # 取得季度小于等于0的
    _df = _df[_df['_quarter_sub'] < 1]
    # 判断是否有超过n个季度的数据。
    if len(_df) > n:
        # 取得最后的n项数据。
        return _df.tail(n)
    return _df


def quarter_sub(quarter_1, quarter_2):
    """
        Description : 季度减法。判断2个季度中间相差几个季度。
        Arg :
        Returns :
        Raises	 :
    """
    # 假设相等，就返回0啦
    if (quarter_1 == quarter_2):
        return 0
    # 这个格式是"2017-1", 表示2017年第一个季度
    _year_1, _quarter_1 = quarter_1.split('-')
    _year_2, _quarter_2 = quarter_2.split('-')
    _year_1 = int(_year_1)
    _year_2 = int(_year_2)
    _quarter_1 = int(_quarter_1)
    _quarter_2 = int(_quarter_2)
    # 判断年份是否大于吧
    if _year_1 > _year_2:
        # 如果大于，就表示是正数了。
        return (_year_1 - _year_2 - 1) * 4 + _quarter_1 + (4 - _quarter_2)
    elif _year_1 == _year_2:
        # 如果是同一年的，就季度相减吧
        return _quarter_1 - _quarter_2
    else:
        # 如果小于的年份
        return (_year_1 - _year_2 + 1) * 4 - (4 - _quarter_1) - _quarter_2


# 将如上的函数保障成func函数
quarter_sub_func = np.frompyfunc(quarter_sub, 2, 1)


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
    _df = stone.select(finance_type, where=[code_where, year_quarter_where])
    if _df is None or len(_df) == 0:
        return None
    _dict = _df.to_dict()
    _dict_2 = {}
    for _key, _value in _dict.items():
        # 判断这个_value是否也是这字典
        if (isinstance(_value, dict)):
            _dict_2[_key] = _value[_df.index[0]]
        else:
            _dict_2[_key] = _value
    return _dict_2


def get_stock_basics(code):
    """
        Description : 取得某个股票的基本信息，请注意这个只是取得最近的基本信息。
        不能设定时间的。
        Arg :
        Returns :
        Raises	 :
    """
    code_where = 'index=="{}"'.format(get_tushare_code(code))
    _df = stone.select(str_stock_basic, where=[code_where])
    if _df is None or len(_df) == 0:
        return None
    _dict = {}
    _dict['code'] = _df.index[0]
    for _key in _df.keys():
        _dict[_key] = _df[_key][0]
    return _dict


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


def df_drop_duplicates(finance_type):
    """
        Description : 将指定财务类别去重复
        Arg :
        Returns :
        Raises	 :
    """
    _df = stone.select(finance_type)
    _df = _df.drop_duplicates(['code', 'year_quarter'])
    # 重新赋值
    stone.append(finance_type, _df, format='table', append=False)
    pass


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
                try:
                    _fun(year, quarter)
                except:
                    pass


if __name__ == '__main__':
    # print(get_finance_data(str_report, '000002', 2017, 1))
    # print(get_stock_basics('000002'))
    # init_stock_basics()
    # stone.remove(str_report)
    # init_data()
    # print(get_all_finance_data(str_report, '000001'))
    # print(get_finance_data(str_report, '300419', 2014, 3))
    # print(quarter_sub('2017-1', '2016-2'))
    # print(quarter_sub('2015-1', '2016-2'))
    print(get_last_finance_data_2(str_report, ['000001', '000002']))
    pass
