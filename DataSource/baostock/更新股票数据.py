import baostock as bs
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import os

_file_path_ = os.path.split(os.path.realpath(__file__))[0]

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)



# 这里要遍历所有的股票
dt = pd.read_csv("stock_industry.csv", sep=',', encoding="utf_8_sig")
codes = list(dt.loc[:, 'code']) # 取得所有的股票名称

# 这里追加指数数据
indexs = [
    'sh.000001', # 上证
    'sz.399106'  # 深证
]

# 追加
codes.extend(indexs)

# 然后用进度条
for i  in tqdm(range(len(codes))):
    _code_name = codes[i]
    is_need_download_all = True
    # 这里先判断一下是否有这个文件
    csv_path = os.path.join(_file_path_, "k线数据", f'{_code_name}.csv')
    if os.path.exists(csv_path):
        dt2 = pd.read_csv(csv_path,sep=',')  # 这里仅仅是读取
        # 取得最后的日期
        if len(dt2) > 0:
            late_date = dt2.iloc[-1,0]
            # 然后下载数据
            rs = bs.query_history_k_data_plus(
                _code_name,
                "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                start_date=late_date, # end_date='2021-12-21',
                frequency="d", adjustflag="2")
            # 保存在下边
            data_list = []
            while (rs.error_code == '0') & rs.next():
                # 获取一条记录，将记录合并在一起
                data_list.append(rs.get_row_data())
            result = pd.DataFrame(data_list, columns=rs.fields)
            # 这里比较一下是否有更新,我这里检查的是开盘价
            if len(result) == 0:
                is_need_download_all = False
            elif dt2.iloc[-1,2] == float(result.iloc[0, 2]):
                is_need_download_all = False
                # 这里做一下拼接
                dt4 = dt2.dropna()
                dt5 = result.iloc[1:, :].dropna()
                dt3 = pd.concat([dt4, dt5 ], axis=0)
                dt3.to_csv(csv_path, index=False,encoding='utf_8_sig')

    
    # 判断是否需要下载全部
    if is_need_download_all:
        rs = bs.query_history_k_data_plus(
            _code_name,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            start_date='2010-01-01', # end_date='2021-12-21',
            frequency="d", adjustflag="2")
        # 保存在
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        # 然后要保存在目录中。
        result.to_csv(csv_path, index=False,encoding='utf_8_sig')

#### 登出系统 ####
bs.logout()