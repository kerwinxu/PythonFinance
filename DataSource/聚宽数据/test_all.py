# 这个是用测试来实现的各种测试。
import pytest
import os
import pandas as pd
import datasource as DataSource

file_dir = os.path.dirname(os.path.realpath(__file__))

def test_csv_to_sqlite():
    """测试csv的是否已经导入到sql中
        检查最后一支股票的最后收盘价和日期是否相同。
    """
    # 首先取得第一个csv文件
    csv_dir = os.path.join(file_dir, "最新数据") # 目录
    files_names = os.listdir(csv_dir) # 目录下的文件
    file_paths = [os.path.join(csv_dir, i) for i in files_names if i.endswith('.csv')] # 拼接目录
    # 我这里只是读取第一个csv的
    # 判断是否有文件
    assert len(file_paths) > 0
    csv_path = file_paths[-1] # 最后一个csv文件
    df = pd.read_csv(csv_path) # 导入
    df = df.rename(columns={'Unnamed: 0': 'code'})
    codes = df['code'].unique() # 取得这一列不重复的值
    # 取得最后一个股票
    code = codes[-1]
    df2 = df.loc[df['code'] == code, :].iloc[-1] # 取得这一支股票的最后的数据
    last_close_by_csv = df2['close'] # 最后的收盘价
    last_date_by_csv = df2['date'] # 最后的日期
    last_date_by_csv = pd.to_datetime(last_date_by_csv)
    # 然后这里从sqlite中取得
    df3 = DataSource.getData(code) # 从sqlte中取得这个股票
    df4 = df3.iloc[-1] # 最后的数据,这个不需要判断code了
    last_close_by_sqlite = df4['close'] # 最后的收盘价
    last_date_by_sqlite = df4.name[1] # 最后的日期，请注意索引是一个二元的元组，(股票代码, 日期)
    # 做判断
    assert last_close_by_csv == last_close_by_sqlite
    assert last_date_by_csv == last_date_by_sqlite
    
    


if __name__ == '__main__':
    # 注意，这个只是检查这一个文件，不扫描。
    # pytest.main([os.path.realpath(__file__)])
    pytest.main() # 扫描模式