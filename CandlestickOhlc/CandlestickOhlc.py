#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-03 20:47:16
# Last Change:  2017-10-07 20:27:14
# File Name: simple_1.py

from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from mpl_finance import candlestick_ohlc
import pandas as pd
import datetime
import matplotlib.pyplot as plt   # Import matplotlib
import pylab
import numpy as np


def candlestick_ohlc(dat, stick="day", shareseries=None, otherseries=None):
    """
    这个方法用来绘制k线图的，现在已经可以显示k线图，附加在主图上的指标和其他单独显示的字表。
        :param dat: pandas DataFrame object with datetime64 index, and float columns "Open", "High", "Low", and "Close", likely created via DataReader from "yahoo"
        :param stick: A string or number indicating the period of time covered by a single candlestick. Valid string inputs include "day", "week", "month", and "year", ("day" default), and any numeric input indicates the number of trading days included in a period
        :param shareseries:  这个是共用在主图上的An iterable that will be coerced into a list, containing the columns of dat that hold other series to be plotted as lines
        :param otherseries: 其他的图形，比如KDJ，RSI之类的

    This will show a Japanese candlestick plot for stock data stored in dat, also plotting other series if passed.
    """
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays 获得每周一的日期数据，这个当主要刻度
    alldays = DayLocator()              # minor ticks on the days 获得美日数据，这个当次要刻度
    # dayFormatter = DateFormatter('%d')      # e.g., 12
    # ax.xaxis.set_major_formatter(mondayFormatter)，用这个来设定格式

    # Create a new DataFrame which includes OHLC data for each period specified by stick input
    # 只是取得开盘价，最高价，最低价和收盘价，好像这种会自动添加日期。
    transdat = dat.loc[:, ["Open", "High", "Low", "Close"]]
    # 接下来判断周期，
    # 如果是用字符串表示的
    if (type(stick) == str):
        # 判断如果是日线
        if stick == "day":
            # 就用原先数据啦
            plotdat = transdat
            stick = 1    # Used for plotting
        # 判断如果是周线，月线和年限
        elif stick in ["week", "month", "year"]:
            # 如果是周线。
            if stick == "week":
                # pandas提供to_datetime方法将代表时间的字符转化为Timestamp对象, 这个对象是时间戳：
                transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1])     # Identify weeks
            elif stick == "month":
                transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month)        # Identify months
            transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0])      # Identify years
            grouped = transdat.groupby(list(set(["year", stick])))       # Group by year and other appropriate variable
            plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []})         # Create empty data frame containing what will be plotted
            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0, 0],
                                                       "High": max(group.High),
                                                       "Low": min(group.Low),
                                                       "Close": group.iloc[-1, 3]},
                                                      index=[group.index[0]]))
            if stick == "week":
                stick = 5
            elif stick == "month":
                stick = 30
            elif stick == "year":
                stick = 365

    elif (type(stick) == int and stick >= 1):
        # 下边这个应该算是分钟图了吧
        transdat["stick"] = [np.floor(i / stick) for i in range(len(transdat.index))]
        grouped = transdat.groupby("stick")
        plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []})         # Create empty data frame containing what will be plotted
        for name, group in grouped:
            plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0, 0],
                                                   "High": max(group.High),
                                                   "Low": min(group.Low),
                                                   "Close": group.iloc[-1, 3]},
                                                  index=[group.index[0]]))

    else:
        raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')

    # 如下是绘图了
    # Set plot parameters, including the axis object ax used for plotting
    fig, ax = plt.subplots()
    # 如下是判断是否有别的子图
    if(otherseries is not None):
        if type(otherseries) != list:
            otherseries = [otherseries]
        zitu_count = len(otherseries)
        zhutu_size = 2
        # 永远算主图为2个子图大小
        fig = plt.figure(1)
        # 用表格的形式来表示分割大小。
        fengedaxiao = (zhutu_size+zitu_count, 1)
        # 设置主图吧
        ax = plt.subplot2grid(fengedaxiao, (0, 0), rowspan=zhutu_size)
        # 设置子图
        k = zhutu_size
        # 设置单独的子图
        while k < zitu_count+zhutu_size:
            # 要显示的列
            col_name_1 = otherseries[k-zhutu_size]
            # sharex的意思是共享X轴
            ax2 = plt.subplot2grid(fengedaxiao, (k, 0), sharex=ax)
            # 绘制图形啦，只是绘制一个图形而已
            dat.loc[:, col_name_1].plot(ax=ax2)
            # 比如得加str转换一个格式
            ax2.set_title(str(col_name_1))
            k = k + 1
            pass

    # fig 相当于画布了
    # ax 相当于子图
    # fig.subplots_adjust(bottom=0.2)
    # 因为数据有多少的问题，如下是判断，如果天数大于730天，就设置清晰点。
    if plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        # 如果大于730天，就得显示年了。
        weekFormatter = DateFormatter('%b %d, %Y')
    # 设置主要的时间刻度
    ax.xaxis.set_major_formatter(weekFormatter)

    ax.grid(True)

    # Create the candelstick chart
    candlestick_ohlc(ax, list(zip(list(pylab.date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), plotdat["High"].tolist(),
                                  plotdat["Low"].tolist(), plotdat["Close"].tolist())),
                     colorup="red", colordown="green", width=stick * .4)

    # Plot other series (such as moving averages) as lines
    if shareseries is not None:
        if type(shareseries) != list:
            shareseries = [shareseries]
        dat.loc[:, shareseries].plot(ax=ax, lw=1.3, grid=True)

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    plt.show()


if __name__ == "__main__":
    # We will look at stock prices over the past year, starting at January 1, 2016
    start = datetime.datetime(2016, 1, 1)
    end = datetime.date.today()
    # Let's get Apple stock data; Apple's ticker symbol is AAPL
    # First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance), third is the start date, fourth is the end date
    # apple = web.DataReader("AAPL", "yahoo", start, end)
    import sys
    sys.path.append("../FinanceDataSource")
    import FinanceDataSource
    # yahoo_s_p_500 = init_data.get_data(init_data.str_pandas_datareader, init_data.yahoo_s_p_500)
    # pandas_candlestick_ohlc(yahoo_s_p_500)
    data = FinanceDataSource.get_tonghuashun_data(FinanceDataSource.tonghuashun_AGUSDO)

    import talib
    data["20d"] = talib.MA(data["Close"].as_matrix(), 20)
    data["120d"] = talib.MA(data["Close"].as_matrix(), 120)
    candlestick_ohlc(data, stick="day", shareseries=["20d"], otherseries=["20d", "120d"])
