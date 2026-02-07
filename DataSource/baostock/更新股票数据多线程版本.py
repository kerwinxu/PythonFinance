import baostock as bs
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import multiprocessing as mp
import os

#! 多线程版本不能成功

_file_path_ = os.path.split(os.path.realpath(__file__))[0]
COLUMNS = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"
START_DATE = '2010-01-01'
INDUSTRY_PATH = os.path.join(_file_path_, "stock_industry.csv")
INDEX_PATH = os.path.join(_file_path_, '指数.xlsx')


def thread_update_code(code_name):
    # 更新股票的多进程版本
    lg = bs.login()
    rs = bs.query_history_k_data_plus(
        code_name,
        COLUMNS,
        start_date=START_DATE, # end_date='2021-12-21',
        frequency="d", adjustflag="1")
    # 保存在
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    # 然后要保存在目录中。
    csv_path = os.path.join(_file_path_, "k线数据", f'{code_name}.csv')
    result.to_csv(csv_path, index=False,encoding='utf_8_sig')
    bs.logout()


def main():
    # 这里要遍历所有的股票
    dt = pd.read_csv(INDUSTRY_PATH, sep=',', encoding="utf_8_sig")
    codes = list(dt.loc[:, 'code']) # 取得所有的股票名称
    # 这里追加指数数据
    dt_index=pd.read_excel(INDEX_PATH)
    indexs = list(dt_index['指数代码'])
    # 追加
    codes.extend(indexs)
    # 这里用多线程来做
    # 创建进程池
    num_processes = mp.cpu_count()
    pool = mp.Pool(4)

    # 执行任务并显示进度条
    with tqdm(total=len(codes)) as pbar:
        for code_name in codes:
            pool.apply_async(thread_update_code, 
                            args=(code_name,),
                            callback=lambda _: pbar.update(1))

    # 关闭进程池
    pool.close()
    pool.join()    

if __name__ == '__main__':
    main()