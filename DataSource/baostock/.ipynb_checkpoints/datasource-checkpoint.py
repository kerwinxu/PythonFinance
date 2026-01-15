# 这个是作为数据源的脚本
import pandas as pd
import os
_file_path_ = os.path.split(os.path.realpath(__file__))[0]

def get_data(code):
	csv_path = os.path.join(_file_path_, "k线数据", f'{code}.csv')
    # 这里要判断是否有这个数据
    if os.path.exists(csv_path):
    	dt = pd.read_csv(csv_path,sep=',',parse_dates=['date'], index_col=0)
    	return dt
    else:
        return None

def get_codes():
	csv_path = os.path.join(_file_path_, "stock_industry.csv")
	dt = pd.read_csv(csv_path, sep=',',encoding='utf-8')
	return list(dt['code'])

def get_zz500_codes():
	csv_path = os.path.join(_file_path_, "zz500_stocks.csv")
	dt = pd.read_csv(csv_path, sep=',',encoding='utf-8')
	return list(dt['code'])