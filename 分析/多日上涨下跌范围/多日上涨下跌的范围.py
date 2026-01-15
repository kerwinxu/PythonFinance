#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
import os


# In[14]:


# 这里导入数据
df = pd.read_csv("../../数据获取/聚宽数据/最新数据.csv")


# In[48]:


df.head()


# In[47]:


df.columns = ['id','i', 'Date','Open','High','Low','Close','Volume']


# In[ ]:





# In[17]:


num_days = 5 # 看几天的
ranges = []
for id in set(df['id']):
    # 对每一只股票进行遍历
    df2 = df[df['id']==id].copy()
    # 然后
    df2['Close2'] = df2['Close'].shift(num_days)
    df2['range'] = (df2['Close']-df2['Close2'])/df2['Close2'] * 100
    ranges.extend([int(i) for i in df2['range'] if not np.isnan(i)])


# In[18]:


len(ranges)


# In[23]:


len(set(ranges))


# In[28]:


list(set(ranges))[-10:]


# In[30]:


# 我这里计算每个幅度的数量
df3 = pd.value_counts(ranges)
df3.head(10)


# In[33]:





# In[34]:


df3 = df3.sort_index()


# In[35]:


df3.head(10)


# In[38]:


# plt.plot(df3.index, df3.values)


# In[43]:


df3[df3.index>50]


# In[44]:


sum(df3[df3.index>50])


# In[45]:


sum(df3[df3.index>50])/len(ranges)


# In[57]:


# 我这里要看看k线图
dest_dir = "N日上涨50%的k线图"
if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)
import  mplfinance as mpf


# In[84]:


i = 1
rise_threshold = 50
import os
before = 30 # 前多少天的数据
for id in set(df['id']):
    # 对每一只股票进行遍历
    df2 = df[df['id']==id].copy()
    
    # 然后重新设置
    df2['Date']=pd.to_datetime(df2['Date'])
    df2 = df2.set_index('Date')
    # 这里首先计算5日涨幅
    df2['Close2'] = df2['Close'].shift(num_days)
    # 然后计算涨幅
    df2['rise']  =  (df2['Close']-df2['Close2'])/df2['Close2'] * 100
    df2['threshold'] = 0
    threshold_index = list(df2.columns).index('threshold')
    df2.loc[df2['rise'] > rise_threshold, 'threshold'] = 1
    # 然后移动
    df2['threshold2'] = df2['threshold'].shift(0-before)
    threshold2_index = list(df2.columns).index('threshold2')
    threshold2_index = list(df2.columns).index('threshold2')
    # 这里就开始画图了
    # print(list([k for k in df2['rise'] if k > rise_threshold]))
    # print(df2[df2['threshold2'] == 1])
    # print(list(df2['threshold']))
    # print(df2.loc[df2['rise'] > rise_threshold])
    for j in range(len(df2)):
        # 这里要判断
        if df2.iloc[j, threshold2_index] == 1.0:
            # 这里表示要截取
            df3 = df2.iloc[j:j+before,:]
            # 然后以这个绘图
            mydpi = 300
            fig1, _ = mpf.plot(df3,
                           type='candle',
                           style='yahoo',
                           figsize =(3240/mydpi,2520/mydpi), 
                           volume=True,
                           axisoff=True,
                           returnfig=True, 
                           scale_padding=0.2)
            # 这里生成文件名
            dest_path = os.path.join(dest_dir, "{}-{}-{}.jpg".format(i, id,df2.index[j].strftime("%Y-%m-%d")))
            i += 1
            fig1.savefig(dest_path,dpi=mydpi)
            plt.clf()
            plt.close()
            print(dest_path)
    
    


# In[ ]:




