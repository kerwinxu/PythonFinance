#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: e:\Program\python\PythonFinance\FinanceDataSource\tushare_data\tushare_data_3.py
# Project: e:\Program\python\PythonFinance\FinanceDataSource\tushare_data
# Created Date: Thursday, April 5th 2018, 8:40:05 pm
# Author: kerwin xu
# -----
# Last Modified:
# Modified By:
# -----
# Copyright (c) 2018 kerwin_xu
#
# 这个是用mysql实现的数据。
# 我打算每个财务报表做一个表格，
# 基本上一个是基本表格，一个是其他财务表格。
# 在执行sql方面，我打算用2方面来执行。
# 其中要取得数据的用pandas的read_sql来做。
# 而要保存更新或者插入数据的用to_sql来做。
###

import pandas as pd
import numpy as np
import tushare as ts
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import String, Integer, Float, Date, VARCHAR, func
# from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import logging
import datetime

# 定义引擎
DB_CONNECT_STRING = "mysql+pymysql://business:nicaibudaola111@localhost/business_one"
engine = create_engine(DB_CONNECT_STRING, connect_args={
    'charset': 'utf8'}, echo=True)  # 创建数据库引擎
# 绑定元信息
metadata = MetaData(engine)

DB_Session = sessionmaker(bind=engine)  # 数据库会话类
session = DB_Session()  # 数据库会话类的实例

# 我首先建立表吧
# 上市公司基本情况。因为这个表只是最近的，所以这个表每天更新一次。
stock_basics_table = Table("tushare_stock_basics", metadata,
                           Column("ID", Integer, primary_key=True),
                           Column('code', VARCHAR(20)),
                           Column("name", VARCHAR(30)),  # 股票名称
                           Column("area", VARCHAR(20)),  # 股票地区
                           Column("industry", VARCHAR(30)),  # 所属行业
                           Column("timeToMarket", Date),  # 上市日期
                           Column("pe", Float),  # 市盈率
                           Column("outstanding", Float),  # 流通股本（亿——
                           Column("totals", Float),  # 总股本
                           Column("totalAssets", Float),  # 总资产
                           Column("liquidAssets", Float),  # 流动资产
                           Column("fixedAssets", Float),  # 固定资产
                           Column("reserved", Float),  # 公积金
                           Column("reservedPerShare", Float),  # 每股公积金
                           Column("esp", Float),  # 每股收益
                           Column("bvps", Float),  # 每股净资产
                           Column("pb", Float),  # 市净率
                           Column("undp", Float),  # 未分利润
                           Column("perundp", Float),  # 每股未分配
                           Column("rev", Float),  # 收入同比
                           Column("profit", Float),  # 利润同比
                           Column("gpr", Float),  # 毛利率
                           Column("npr", Float),  # 净利润率
                           Column("holders", Float)  # 股东人数
                           )

# 业绩报告总表
stock_report_data = Table("tushare_stock_report_data", metadata,
                          Column("ID", Integer, primary_key=True),
                          Column("code", VARCHAR(20)),  # 股票代码
                          Column("name", VARCHAR(30)),  # 股票名称
                          Column("eps", Float),  # 每股收益
                          Column("eps_yoy", Float),  # 每股收益同比
                          Column("bvps", Float),  # 每股净资产
                          Column("roe", Float),  # 净资产收益率
                          Column("epcf", Float),  # 每股现金流量（元）
                          Column("net_profits", Float),  # 净利润（万元）
                          Column("profits_yoy", Float),  # 净利润同比
                          Column("distrib", String(100)),  # 分配方案
                          Column("report_date", Date),  # 报表发布日期
                          Column("year", Integer),  # 年份
                          Column("quarter", Integer))

stock_profit_data = Table("tushare_stock_profit_data", metadata,
                          Column("ID", Integer, primary_key=True),
                          Column("code", VARCHAR(20)),  # 股票代码
                          Column("name", VARCHAR(30)),  # 股票名称
                          Column("roe", Float),  # 净资产收益率
                          Column("net_profit_ratio", Float),  # 净利率
                          Column("gross_profit_rate", Float),  # 毛利率(%)
                          Column("net_profits", Float),  # 净利润(万元)
                          Column("eps", Float),  # 每股收益
                          Column("business_income", Float),  # 营业收入(百万元)
                          Column("bips", Float),  # 每股主营业务收入(元)
                          Column("year", Integer),  # 年份
                          Column("quarter", Integer))

stock_operation_data = Table("tushare_stock_operation_data", metadata,
                             Column("ID", Integer, primary_key=True),
                             Column("code", VARCHAR(20)),  # 股票代码
                             Column("name", VARCHAR(30)),  # 股票名称
                             Column("arturnover", Float),  # 应收账款周转率(次)
                             Column("arturndays", Float),  # 应收账款周转天数(天)
                             Column("inventory_turnover", Float),  # 存货周转率(次)
                             Column("inventory_days", Float),  # 存货周转天数(天)
                             Column("currentasset_turnover",
                                    Float),  # 流动资产周转率(次)
                             Column("currentasset_days", Float),  # 流动资产周转天数(天)
                             Column("year", Integer),  # 年份
                             Column("quarter", Integer))


stock_growth_data = Table("tushare_stock_growth_data", metadata,
                          Column("ID", Integer, primary_key=True),
                          Column("code", VARCHAR(20)),  # 股票代码
                          Column("name", VARCHAR(30)),  # 股票名称
                          Column("mbrg", Float),  # 主营业务收入增长率(%)
                          Column("nprg", Float),  # 净利润增长率(%)
                          Column("nav", Float),  # 净资产增长率
                          Column("targ", Float),  # 总资产增长率
                          Column("epsg", Float),  # 每股收益增长率
                          Column("seg", Float),  # 股东权益增长率
                          Column("year", Integer),  # 年份
                          Column("quarter", Integer))

stock_debtpaying_data = Table("tushare_stock_debtpaying_data", metadata,
                              Column("ID", Integer, primary_key=True),
                              Column("code", VARCHAR(20)),  # 股票代码
                              Column("name", VARCHAR(30)),  # 股票名称
                              Column("currentratio", Float),  # 流动比率
                              Column("quickratio", Float),  # 速动比率
                              Column("cashratio", Float),  # 现金比率
                              Column("icratio", Float),  # 利息支付倍数
                              Column("sheqratio", Float),  # 股东权益比率
                              Column("adratio", Float),  # 股东权益增长率
                              Column("year", Integer),  # 年份
                              Column("quarter", Integer))

stock_cashflow_data = Table("tushare_stock_cashflow_data", metadata,
                            Column("ID", Integer, primary_key=True),
                            Column("code", VARCHAR(20)),  # 股票代码
                            Column("name", VARCHAR(30)),  # 股票名称
                            Column("cf_sales", Float),  # 经营现金净流量对销售收入比率
                            Column("rateofreturn", Float),  # 资产的经营现金流量回报率
                            Column("cf_nm", Float),  # 经营现金净流量与净利润的比率
                            Column("cf_liabilities", Float),  # 经营现金净流量对负债比率
                            Column("cashflowratio", Float),  # 现金流量比率
                            Column("year", Integer),  # 年份
                            Column("quarter", Integer))


def create_table():
    """建立表"""
    stock_basics_table.create(checkfirst=True)
    stock_report_data.create(checkfirst=True)
    stock_profit_data.create(checkfirst=True)
    stock_operation_data.create(checkfirst=True)
    stock_growth_data.create(checkfirst=True)
    stock_debtpaying_data.create(checkfirst=True)
    stock_cashflow_data.create(checkfirst=True)


def insert_into(df, tb):
    """
        Description :
        Arg :
        Returns :
        Raises	 :
    """
    _items = tb.columns.items()
    _items_count = len(_items)
    # 注意这个if_exists，不能用replease,用那个是先删除这个表，再新建的方式。
    df.to_sql(tb.fullname, engine,
              if_exists='append', index=False,
              dtype={_items[i][0]: _items[i][1].type
                     for i in range(_items_count)},
              chunksize=1000)


def delete_data(_tb, _filter):
    """删除数据的。

    Arguments:
        _tb {[type]} -- [Table类型]
        _filter {[type]} -- [筛选器]

    Returns:
        [bool] -- [是否成功删除的]
    """

    try:
        # pd.read_sql("use business_one")
        # pd.read_sql("SET SQL_SAFE_UPDATES=0")
        # pd.read_sql(sql)
        # pd.read_sql("SET SQL_SAFE_UPDATES=1 ")
        session.query(_tb).filter(_filter).delete(synchronize_session=False)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logging.error(e)
    return False


def update_table_basics():
    """更新表"""
    # 更新基本情况的
    _df_basics = ts.get_stock_basics()
    _df_basics['code'] = _df_basics.index  # 默认这个不是这个名称
    # session.execute("drop table {}".format(stock_basics_table.fullname))
    if(delete_data(stock_basics_table, True)):
        stock_basics_table.create(checkfirst=True)
        insert_into(_df_basics, stock_basics_table)
    else:
        logging.error("没有成功删除数据。")
    # 如下是更新业绩总表的。
    # 业绩总表，我打算这样子，首先删除今年和去年的所有数据。
    # 然后从股市开始的数据开始，判断每个季度的财报是否有，如果没有，就下载并插入。
    # 因为几个财务指标都是差不多的，所以还是放在一个方法中吧


def update_table_2(_tb, fun_get):
    # 首先删除今年和去年的数据
    this_year = datetime.datetime.now().year
    pre_year = this_year - 1
    delete_data(_tb, _tb.c.year == this_year)
    delete_data(_tb, _tb.c.year == pre_year)
    # 我这里都是以2000年开始吧
    # 季度当然是4个季度啦
    for _year in range(2000, this_year + 1):
        for _quarter in range(1, 5):
            # 首先看看是否有相关数据
            _count = session.query(_tb).filter(
                _tb.c.year == _year).filter(_tb.c.quarter == _quarter).count()
            if(_count == 0):
                # 如果没有，就新建啦。
                try:
                    _df = fun_get(_year, _quarter)
                    # 要判断是否取得数据。
                    if len(_df) == 0:
                        continue
                    _df['year'] = _year
                    _df['quarter'] = _quarter
                    _df = _df.replace({np.nan: 0, '--': 0})
                    # report_date 也需要更改
                    # 但因为有些项目没有这个发布日期，所以这里有个判断
                    if("report_date" in _df.columns.tolist()):
                        pass
                        _df['month'] = _df['report_date'].str[:2]
                        # 转化类型，
                        _df['month'] = pd.to_numeric(_df['month'])
                        # 转成季度
                        _df['month'] = _df['month'] / 3
                        # 判断是否是明年，假设他们别延误超过1年发布吧。
                        _b = _quarter < _df['month']
                        # 然后修改啦
                        for i in range(len(_df)):
                            if(_b[i]):
                                _d = str(_year) + "-" + _df['report_date'][i]
                                # 因为出现一个特殊的数据2009-02-29，这个日期肯定是错误的啦所以这里要有个判断。
                                try:
                                    datetime.date.strftime(_d)
                                    _df.loc[i, 'report_date'] = _d
                                except Exception as ex:
                                    _df.loc[i, 'report_date'] = str(
                                        _year) + "-" + str(_df['report_date'][i])[:2] + "-01"
                            else:
                                _d = str(_year + 1) + "-" + \
                                    _df['report_date'][i]
                                try:
                                    datetime.date.strftime(_d)
                                    _df.loc[i, 'report_date'] = _d
                                except Exception as ex:
                                    _df.loc[i, 'report_date'] = str(
                                        _year + 1) + "-" + str(_df['report_date'][i])[:2] + "-01"
                        del _df['month']
                    insert_into(_df, _tb)
                except Exception as ex:
                    continue


def session_close():
    session.close()


def auto_update():
    """
    这个方法的作用是自动更新
    """
    create_table()
    update_table_basics()
    update_table_2(stock_report_data, ts.get_report_data)
    update_table_2(stock_profit_data, ts.get_profit_data)
    update_table_2(stock_operation_data, ts.get_operation_data)
    update_table_2(stock_growth_data, ts.get_growth_data)
    update_table_2(stock_debtpaying_data, ts.get_debtpaying_data)
    update_table_2(stock_cashflow_data, ts.get_cashflow_data)
    session_close()


def get_fundamentals(q):
    # 首先判断这个q是sql还是query吧。
    if(isinstance(q, str)):
        return pd.read_sql(q, engine)
    elif(isinstance(q, sqlalchemy.orm.query.Query)):
        return pd.read_sql(q.statement, engine)
    else:
        return None


if __name__ == "__main__":
    auto_update()
    session_close()
