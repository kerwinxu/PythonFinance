import baostock as bs
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import os
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

_file_path_ = os.path.split(os.path.realpath(__file__))[0]
START_DATE = '2010-01-01'

# 这个脚本支持只是读取最后的数据，而不是全部数据都读取,请注意，这里改成后复权。。。

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 这里要遍历所有的股票
dt = pd.read_csv(os.path.join(_file_path_,"stock_industry.csv"), sep=',', encoding="utf_8_sig")
codes = list(dt.loc[:, 'code']) # 取得所有的股票名称

# 这里是取得交易日的
last_updateDate = dt['updateDate'].max() # 取得最后的更新时间 
last_updateDate = datetime.strptime(last_updateDate, f'%Y-%m-%d') # 转成日期
last_updateDate = last_updateDate + timedelta(days=4) # 日期加5天
last_updateDate = min([datetime.now() , last_updateDate]) # 到这里可以认为是股市最后的交易日。


#### 获取交易日信息 ####
# 我这里是取得交易日前面一个月的
_start_date = last_updateDate + timedelta(days=-30) 
_start_date = datetime.strftime(_start_date, f'%Y-%m-%d')
rs = bs.query_trade_dates(start_date=_start_date, end_date=datetime.strftime(datetime.now(), f'%Y-%m-%d'))
print('query_trade_dates respond error_code:'+rs.error_code)
print('query_trade_dates respond  error_msg:'+rs.error_msg)
#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
result2 = result.loc[result['is_trading_day'] == '1', :]
print(result2.head())
last_updateDate = result2.iat[-1, 0]
print(f'最后的交易日:{last_updateDate}')



# 这里追加指数数据
dt_index=pd.read_excel(os.path.join(_file_path_,'指数.xlsx'))
indexs = list(dt_index['指数代码'])

# 追加
codes.extend(indexs)

COLUMNS = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"

import functools
import sys

import ctypes
import threading


class ThreadKiller(threading.Thread):
    """separate thread to kill TerminableThread"""

    def __init__(self, target_thread, exception_cls, repeat_sec=2.0):
        threading.Thread.__init__(self)
        self.target_thread = target_thread
        self.exception_cls = exception_cls
        self.repeat_sec = repeat_sec
        self.daemon = True

    def run(self):
        """loop raising exception incase it's caught hopefully this breaks us far out"""
        while self.target_thread.is_alive():
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.target_thread.ident),
                                                       ctypes.py_object(self.exception_cls))
            self.target_thread.join(self.repeat_sec)
            

class TerminableThread(threading.Thread):
    """a thread that can be stopped by forcing an exception in the execution context"""

    def terminate(self, exception_cls, repeat_sec=2.0):
        if self.is_alive() is False:
            return True
        killer = ThreadKiller(self, exception_cls, repeat_sec=repeat_sec)
        killer.start()

def timeout(sec, raise_sec=1):
    """
    timeout decorator
    :param sec: function raise TimeoutError after ? seconds
    :param raise_sec: retry kill thread per ? seconds
        default: 1 second
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            err_msg = f'Function {func.__name__} timed out after {sec} seconds'

            if sys.platform != 'win32':
                import signal

                def _handle_timeout(signum, frame):
                    raise TimeoutError(err_msg)

                signal.signal(signal.SIGALRM, _handle_timeout)
                signal.alarm(sec)
                try:
                    result = func(*args, **kwargs)
                finally:
                    signal.alarm(0)
                return result

            else:
                class FuncTimeoutError(TimeoutError):
                    def __init__(self):
                        TimeoutError.__init__(self, err_msg)

                result, exception = [], []

                def run_func():
                    try:
                        res = func(*args, **kwargs)
                    except FuncTimeoutError:
                        pass
                    except Exception as e:
                        exception.append(e)
                    else:
                        result.append(res)

                # typically, a python thread cannot be terminated, use TerminableThread instead
                thread = TerminableThread(target=run_func, daemon=True)
                thread.start()
                thread.join(timeout=sec)

                if thread.is_alive():
                    # a timeout thread keeps alive after join method, terminate and raise TimeoutError
                    exc = type('TimeoutError', FuncTimeoutError.__bases__, dict(FuncTimeoutError.__dict__))
                    thread.terminate(exception_cls=FuncTimeoutError, repeat_sec=raise_sec)
                    raise TimeoutError(err_msg)
                elif exception:
                    # if exception occurs during the thread running, raise it
                    raise exception[0]
                else:
                    # if the thread successfully finished, return its results
                    return result[0]

        return wrapped_func
    return decorator


def pull_data(_code_name):
    is_need_download_all = False
    # 我要看看最少可以读取多少
    # 这里先判断一下是否有这个文件
    csv_path = os.path.join(_file_path_, "k线数据", f'{_code_name}.csv')
    try:
        if os.path.exists(csv_path):
            dt2 = pd.read_csv(csv_path,sep=',')  # 这里仅仅是读取
            # 取得最后的日期
            if len(dt2) > 0:
                # 取得最后的日期
                late_date = dt2.iloc[-1,0]
                # 这里需要计算一下两个日期是否相同。
                if last_updateDate != late_date:
                    # 然后下载数据
                    rs = bs.query_history_k_data_plus(
                        _code_name,
                        COLUMNS,
                        start_date=late_date, # end_date='2021-12-21',
                        frequency="d", adjustflag="1")
                    # 保存在下边
                    data_list = []
                    while (rs.error_code == '0') & rs.next():
                        # 获取一条记录，将记录合并在一起
                        data_list.append(rs.get_row_data())
                    if len(data_list) == 0:
                        print(f'{_code_name},在{late_date}后没有收到数据')
                        # 没有读取到数据，当作全部数据已经读取了。
                        is_need_download_all = False
                    else:
                        result = pd.DataFrame(data_list, columns=rs.fields)
                        # 这里比较一下是否有更新,我这里检查的是开盘价
                        if len(result) == 0:
                            # 这里表示没有读取到数据
                            is_need_download_all = False
                        elif dt2.iat[-1,2] == result.iat[0, 2]:
                            # 这里表示数据可以拼接
                            is_need_download_all = False
                            # 这里做一下拼接
                            dt4 = dt2.dropna()
                            dt5 = result.iloc[1:, :].dropna()
                            dt3 = pd.concat([df for df in [dt4, dt5] if not df.empty], axis=0)
                            dt3.to_csv(csv_path, index=False,encoding='utf_8_sig')
                        else:
                            # 最后这里表示需要读取全部的数据
                            is_need_download_all = True
            else:
                # 如果文件里没有数据，那么也需要全部读取
                is_need_download_all = True
        else:
            # 如果不存在文件，那么需要全部读取
            is_need_download_all = True
    except Exception as err:
        print(f'{_code_name},{err}')

    # 判断是否需要下载全部
    if is_need_download_all:
        rs = bs.query_history_k_data_plus(
            _code_name,
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
        if len(result)>0:
            result.to_csv(csv_path, index=False,encoding='utf_8_sig')
    

# 然后用进度条
for i  in tqdm(range(len(codes))):
    _code_name = codes[i]
    try:
        pull_data(_code_name)
    except Exception as err:
        pass
    time.sleep(1) # 每次运行完毕后停留
        

#### 登出系统 ####
bs.logout()