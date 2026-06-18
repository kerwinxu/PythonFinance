# 这个文件是判断某些文件是否可以正常读取的
import pandas as pd
import os 

code = 'sz.000960'
_file_dir_ = os.path.split(os.path.realpath(__file__))[0]
_csv_path = os.path.join(_file_dir_, "k线数据", f'{code}.csv')

df = pd.read_csv(_csv_path, sep=',')
print(f'数据行数:{len(df)}')