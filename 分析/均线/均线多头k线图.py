import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import os
# from tqdm.notebook import  tqdm
from tqdm import  tqdm
import talib

import  mplfinance as mpf

# 这里导入数据
df = pd.read_csv("../数据获取/聚宽数据/最新数据.csv")
df.columns = ['id','i', 'Date','Open','High','Low','Close','Volume']
df['id2'] =df['id'].shift()
df['i'] = range(len(df))
ids = list(df.loc[df['id'] != df['id2'], 'i']) # 这个是单个股票序号的起始。
ids.append(len(df)-1) # 添加最后1天。

days = 20 # 最多N天的
rises = [[] for _ in range(days)] # 几天的涨幅都在这里边。 
ma_n = [5,10,20,30] # 做这么多多线。
duo_days = []   # 
duo_rises = []
tmp = []
# 前后几天的k线图
before_k = 10
after_k = 10

i_img = 1 # 这个是图片的序号

dest_dir = "均线多头k线图"
if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)
    print("创建文件夹:" + dest_dir)

with tqdm(total=len(ids)) as pbar:
    for j in range(len(ids)-1):
        # 对每一个股票进行遍历
        df2 = df.iloc[ids[j]:ids[j+1],:].copy() # 这里筛选一只股票。
        # 这里要有超过200天的数据
        if len(df2) < 200:
            continue
        # 计算均线
        for m in ma_n:
            df2["Ma{}".format(m)] = talib.SMA(df2['Close'], timeperiod=m)
        # 填充空值,我这里填充0
        df2.fillna(value=0, inplace=True)
        # 这里判断是否是均线多头,我这里要组件表达式
        _tmp = []
        for i in range(len(ma_n)-1):
            _tmp.append("(df2['Ma{}'] > df2['Ma{}'])".format(ma_n[i], ma_n[i+1]))
        _tmp2 = " & ".join(_tmp) 
        # 运行表达式
        df3 = eval("df2[{}].copy()".format(_tmp2))
        # 这里开始统计
        # 这里要看看i所在的列是哪个
        i_index = list(df3.columns).index("i")
        close_index = list(df3.columns).index("Close")
        id_index = list(df3.columns).index("id")
        Date_index = list(df3.columns).index("Date")
        k = 0
        last_i = df3.iat[0, i_index] # 最后一个i的值。
        last_close=df3.iat[0, close_index]
        
        while k < len(df3):
            # 遍历
            if k > 0 and  df3.iat[k, i_index]-df3.iat[k-1, i_index] > 1:
                # 超过1天的，这里要计算天数了
                duo_days.append(df3.iat[k-1, i_index]-last_i+1)
                duo_rises.append((df3.iat[k-1, close_index]-last_close)/last_close*100)
                # 我这里要保存这个均线多头的k线图
                start_i = last_i - before_k  if last_i - before_k >= 0 else 0
                end_i = df3.iat[k-1, i_index] + after_k if df3.iat[k-1, i_index] + after_k < len(df) else len(df)-1
                # 然后截取
                df_plot = df.iloc[start_i:end_i,:]
                df_plot.index=pd.to_datetime(df_plot['Date'])
                # 然后以这个绘图
                mydpi = 96
                fig1, _ = mpf.plot(df_plot,
                               type='candle',
                               style='yahoo',
                               figsize =(800/mydpi,600/mydpi), 
                               volume=True,
                               axisoff=True,
                               returnfig=True, 
                               scale_padding=0.2)
                # 这里生成文件名
                dest_path = os.path.join(dest_dir, "{}-{}-{}-{}.jpg".format(df3.iat[k-1, i_index]-last_i+1,i_img, df3.iat[0, id_index],df3.iat[0,Date_index]))
                i_img += 1
                fig1.savefig(dest_path,dpi=mydpi)
                plt.clf()
                plt.close()
                
                last_i = df3.iat[k, i_index]
                last_close= df3.iat[k, close_index]
                
                pass
            # 
            k += 1
        pbar.update(1)
        # print(list(df3['i']))
        # print(duo_days)
        # break


