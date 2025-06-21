import baostock as bs
import pandas as pd
from datetime import datetime
from tqdm import tqdm


#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)



# 这里要遍历所有的股票
