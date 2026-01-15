#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: e:\Program\python\PythonFinance\FinanceDataSource\tushare_data\tushare_data_2.py
# Project: e:\Program\python\PythonFinance\FinanceDataSource\tushare_data
# Created Date: Tuesday, April 3rd 2018, 10:54:14 pm
# Author: kerwin xu
# -----
# Last Modified:
# Modified By:
# -----
# Copyright (c) 2018 kerwin_xu
#
# 我这个文件用mysql来实现，然后连接方面用Sqlalchemy，但是读取到的数据是pandas，方便计算啊。
###

# 这个文件并没有完成预期。

import tushare as ts
import pandas as pd
from sqlalchemy import String, Integer, Float, Date
from sqlalchemy import Column, MetaData, Table, create_engine, ForeignKey
# from sqlalchemy.sql import select, column, table
from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base
# 定义引擎
DB_CONNECT_STRING = "mysql+pymysql://business:nicaibudaola111@localhost/business_one"
engine = create_engine(DB_CONNECT_STRING, connect_args={
    'charset': 'utf8'}, echo=True)  # 创建数据库引擎
# 绑定元信息
metadata = MetaData(engine)

DB_Session = sessionmaker(bind=engine)  # 数据库会话类
session = DB_Session()  # 数据库会话类的实例

# 麻烦的地方，要建立很多个表啊。
# 股票的代码表
stock_Id = Table("tushare_stock_Id", metadata,
                 Column("ID", String(20), primary_key=True),  # 股票代码
                 Column("name", String(20)),  # 股票名称
                 Column("area", String(20)),  # 股票地区
                 Column("timeToMarket", Date),  # 上市日期
                 )
# 股票财报的年份表，比如2001，2002，只是年份。
stock_report_year = Table("tushare_stock_report_year", metadata,
                          Column("ID", Integer, primary_key=True))
# 股票财报的季度表，其实只有4项，1、2、3、4
stock_report_quarter = Table("tushare_stock_report_quarter", metadata,
                             Column("ID", Integer, primary_key=True))
# 股票财报发布日期
stock_report_date = Table("tushare_stock_report_date", metadata,
                          Column("ID", Date, primary_key=True))
# 上市公司基本情况。因为这个表只是最近的，所以这个表每天更新一次。
stock_basics_table = Table("tushare_stock_basics", metadata,
                           Column('id', Integer, primary_key=True),
                           Column("code", String(20), ForeignKey(
                               "tushare_stock_Id.ID")),  # 股票代码
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
                           Column("holders", Float),  # 股东人数
                           relationship(secondary=stock_Id),
                           )
# 业绩报告总表
stock_report_data = Table("tushare_stock_report_data", metadata,
                          Column('id', Integer, primary_key=True),
                          Column("code", String(20), ForeignKey(
                              "tushare_stock_Id.ID")),  # 股票代码
                          Column("esp", Float),  # 每股收益
                          Column("esp_yoy", Float),  # 每股收益同比
                          Column("bvps", Float),  # 每股净资产
                          Column("roe", Float),  # 净资产收益率
                          Column("epcf", Float),  # 每股现金流量（元）
                          Column("net_profits", Float),  # 净利润（万元）
                          Column("profits_yoy", Float),  # 净利润同比
                          Column("destrib", String(100)),  # 分配方案
                          Column("report_date", Date, ForeignKey(
                              "tushare_stock_report_date.ID")),  # 发布财报的日期
                          Column("year", Integer, ForeignKey(
                              "tushare_stock_report_year.ID")),  # 发布财报的日期
                          Column("quarter", Integer, ForeignKey(
                              "tushare_stock_report_quarter.ID")),  # 发布财报的日期
                          )


def init_stock_basics_create():
    stock_Id.create()
    stock_report_date.create()
    stock_report_quarter.create()
    stock_report_year.create()
    stock_report_data.create()
    stock_basics_table.create()


# def delete_stock_basics_create():
#     stock_Id.delete()
#     stock_report_date.delete()
#     stock_report_quarter.delete()
#     stock_report_year.delete()
#     stock_report_data.delete()
#     stock_basics_table.delete()


def update_basics():
    """这个只是用来更新股票列表的。
    """
    df_basics = ts.get_stock_basics()
    df_basics['code'] = df_basics.index

    pass


def update_data():
    """这个用来更新所有的数据的。
    """

    pass


def get_get_fundamentals():
    """[summary]
    """

    s = stock_basics_table.select(stock_basics_table)
    df1 = pd.read_sql(s, engine)
    print(df1)
    pass


def test2():
    """只是一个试试能否运行的函数"""
    q = session.query(stock_basics_table)
    # s = select([stock_basics_table])
    df = pd.read_sql(q.statement, engine)
    print(df)


init_stock_basics_create()
# test2()
update_basics()
