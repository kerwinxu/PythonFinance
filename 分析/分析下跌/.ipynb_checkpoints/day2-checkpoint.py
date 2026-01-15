import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题


dt = pd.read_csv("下跌结果.csv",  encoding = "utf-8")
dt['日期']=pd.to_datetime(dt['日期']) # 要有日期

dt['星期'] = dt['日期'].dt.dayofweek + 1

# 这里查看一下每个星期几的比例情况


dt['下跌比例'] = dt['下跌数量'] / dt['数量']


print(dt.groupby('星期')['下跌比例'].agg(np.mean))


# 然后显示绘图吧
dt.plot(x = '日期', y='下跌比例', kind = 'line', title = '下跌')

plt.show()

