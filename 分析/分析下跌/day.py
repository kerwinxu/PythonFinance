# 我这个文件想试试股票开盘价比昨天收盘价下跌2%以上的情况

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


down_ratio = 2  # 下跌2%。

dict_day_stock_count = {} # 某天股票的数量
dict_day_down = {}        # 某天下跌股票的数量

base_dir = "../../数据获取/baostock/k线数据"

filenames = os.listdir(base_dir)

for i in range(len(filenames)):
    filename = filenames[i]
    print("{}/{} - {}".format(i, len(filenames), filename))
    if filename[-3:] == 'csv':
        file_path = os.path.join(base_dir, filename)
        dt =  pd.read_csv(file_path)
        if len(dt) > 0:
            # 先统计那些日期有开盘
            for d in list(dt['date']):
                if d not in dict_day_stock_count:
                    dict_day_stock_count[d] = 1

                else:
                    dict_day_stock_count[d] += 1
            # 然后统计下跌的情况
            # dt['close2'] = dt['close'].shift(1)
            # dt2 = dt[dt['open'] <= (100.0 - down_ratio)/100.0 * dt['close2']]
            # for d in list(dt2['date']):
            #     if d not in dict_day_down:
            #         dict_day_down[d] = 1
            #     else:
            #         dict_day_down[d] += 1
            # 如下仅仅是统计当天的
            dt2 = dt[dt['open'] <= dt['close']]
            for d in list(dt2['date']):
                if d not in dict_day_down:
                    dict_day_down[d] = 1
                else:
                    dict_day_down[d] += 1


# 最后合并2个
_date =  dict_day_stock_count.keys() # 日期
_date = [datetime.datetime.strptime(d, "%Y-%m-%d") for d in _date]
_date.sort()
_count1 = [dict_day_stock_count[d.strftime("%Y-%m-%d")] for d in _date] # 当天开票的股票数量
_count2 = [dict_day_down[d.strftime("%Y-%m-%d")] if d.strftime("%Y-%m-%d") in dict_day_down else 0 for d in _date ]  # 当天开盘比昨天收盘跌2%的股票数量

dt3 = pd.DataFrame({
    '日期':_date,
    '数量':_count1,
    "下跌数量":_count2
})

dt3.to_csv("下跌结果.csv", encoding = "utf-8")

dt3['下跌比例'] = dt3['下跌数量'] / dt3['数量']

dt3['下跌比例'].plot(kind='line')


# dt = pd.read_csv("../../数据获取/baostock/k线数据/sh.600000.csv")
# # date	code	open	high	low	close	preclose	volume	amount	adjustflag	turn	tradestatus	pctChg	isST
# dt['close2'] = dt['close'].shift(1)

# # 筛选
# dt2 = dt[dt['close'] <= (100.0 - down_ratio)/100.0 * dt['close2']]

# for d in list(dt2['date']):
#     if d not in dict_day_down:
#         dict_day_down[d] = 1
#     else:
#         dict_day_down[d] += 1

# print(dict_day_down)

