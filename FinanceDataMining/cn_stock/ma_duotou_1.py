
# coding: utf-8

# # 查看A股均线多头的情况

# ## 首先导入相关的库

# In[8]:


import sys
import os
sys.path.append("../../FinanceDataSource")
import FinanceDataSource
import tushare as ts
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns #要注意的是一旦导入了seaborn，matplotlib的默认作图风格就会被覆盖成seaborn的格式
import pandas as pd
import numpy as np
from pandas import DataFrame
from FinanceDataSource import get_cn_stocks
from FinanceDataSource import get_data
from FinanceDataSource import str_cn_stock
from FinanceDataSource

# In[9]:


## 取得所有的股票
_all_cn_stock = get_cn_stocks()


# In[ ]:


class Ma_duotou():
    pass

