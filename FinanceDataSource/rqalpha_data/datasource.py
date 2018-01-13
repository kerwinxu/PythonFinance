# -*- coding: UTF-8 -*-

# Last Change:  2018-01-13 14:53:18
import os
import datetime
import pandas as pd
from rqalpha.data.data_proxy import DataProxy
from rqalpha.utils.datetime_func import convert_int_to_datetime

from rqalpha_data.datetime_utils import to_date_object
from rqalpha_data.quant_utils import to_order_book_id


class DataSource(DataProxy):
    """
    直接使用RQAlpha的全部数据
    """

    def __init__(self, data_bundle_path=None):
        default_bundle_path = os.path.abspath(os.path.expanduser('~/.rqalpha'))
        if data_bundle_path is None:
            data_bundle_path = default_bundle_path
        else:
            data_bundle_path = os.path.abspath(os.path.join(data_bundle_path, '.'))

        data_bundle_path = data_bundle_path + '/bundle'

        self._data_bundle_path = data_bundle_path

        # basic_system_log.debug('rqalpha data bundle path: ' + data_bundle_path)
        # 如果目录不存在，就下载数据
        if not os.path.exists(data_bundle_path):
            self.update(skip_last_date_check=True)

        from rqalpha.data.base_data_source import BaseDataSource
        data_source = BaseDataSource(data_bundle_path)
        super(DataSource, self).__init__(data_source)

        self._last_date_date = None
        self.get_data_last_date()
        # basic_system_log.debug('rqalpha data bundle date: ' + self._last_date_date.strftime('%Y-%m-%d'))

    def get_data_last_date(self):
        """返回最新数据日期"""
        if self._last_date_date is not None:
            return self._last_date_date

        d = self._data_source

        instrument = self.instruments('000001.XSHG')
        raw = d._all_day_bars_of(instrument)
        df = pd.DataFrame.from_dict(raw)
        df['datetime'] = df['datetime'].map(lambda x: pd.to_datetime(str(x)[:8]))

        self._last_date_date = df['datetime'].max().date()

        del df, raw, instrument, d

        return self._last_date_date

    def get_last_trading_day(self):
        """返回最后交易日期"""
        date = datetime.date.today()
        while not self.is_trading_date(date):
            date = date + datetime.timedelta(days=-1)
        return date

    def update(self, skip_last_date_check=False):
        """
        更新最新的远程数据到本地
        """
        if not skip_last_date_check:
            last_trading_day = self.get_last_trading_day()

            data_bundle_path = self._data_bundle_path
            if os.path.exists(data_bundle_path):
                date = self.get_data_last_date()
                if date == last_trading_day:
                    return date  # 数据已经是最新无需下载
                    # basic_system_log.debug('need update data bundle to ' + date.strftime('%Y-%m-%d'))

        data_bundle_path = self._data_bundle_path
        data_bundle_path = data_bundle_path[:len(data_bundle_path) - len('/bundle')]
        from rqalpha import main
        main.update_bundle(data_bundle_path=data_bundle_path)

        if not skip_last_date_check:
            date = self.get_data_last_date()
            return date

    def get_bar(self, order_book_id, dt, frequency='1d'):
        order_book_id = to_order_book_id(order_book_id)
        dt = to_date_object(dt)
        return super(DataSource, self).get_bar(order_book_id=order_book_id, dt=dt, frequency=frequency)

    def history_bars(self,
                     order_book_id,
                     bar_count,
                     frequency,
                     field,
                     dt,
                     skip_suspended=True, include_now=False,
                     adjust_type='pre', adjust_orig=None):
        order_book_id = to_order_book_id(order_book_id)
        dt = to_date_object(dt)
        bars = super(DataSource, self).history_bars(order_book_id=order_book_id,
                                                    bar_count=bar_count,
                                                    frequency=frequency,
                                                    field=field,
                                                    dt=dt,
                                                    skip_suspended=skip_suspended,
                                                    include_now=include_now,
                                                    adjust_type=adjust_type,
                                                    adjust_orig=adjust_orig)
        return bars

    def get_bars(self,
                 order_book_id,
                 dt,
                 bar_count=1,
                 frequency='1d',
                 fields=None,
                 skip_suspended=True,
                 include_now=False,
                 adjust_type='pre',
                 adjust_orig=None,
                 convert_to_dataframe=False):
        order_book_id = to_order_book_id(order_book_id)
        dt = to_date_object(dt)

        if fields is None:
            fields = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'total_turnover']

        bars = super(DataSource, self).history_bars(order_book_id=order_book_id,
                                                    bar_count=bar_count,
                                                    frequency=frequency,
                                                    field=fields,
                                                    dt=dt,
                                                    skip_suspended=skip_suspended,
                                                    include_now=include_now,
                                                    adjust_type=adjust_type,
                                                    adjust_orig=adjust_orig)
        if convert_to_dataframe:
            df = pd.DataFrame.from_dict(bars)
            if 'datetime' in df.columns:
                df['datetime'] = df['datetime'].map(lambda x: convert_int_to_datetime(x))
                df.set_index('datetime', inplace=True)
                df.index.name = ''
            return df

        return bars

    def get_bars_all(self,
                 order_book_id,
                 dt,
                 frequency='1d',
                 fields=None,
                 skip_suspended=True,
                 include_now=False,
                 adjust_type='pre',
                 adjust_orig=None,
                 convert_to_dataframe=False):
        order_book_id = to_order_book_id(order_book_id)
        dt = to_date_object(dt)

        if fields is None:
            fields = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'total_turnover']

        bars = super(DataSource, self).get_bars_all(order_book_id=order_book_id,
                                                    frequency=frequency,
                                                    field=fields,
                                                    dt=dt,
                                                    skip_suspended=skip_suspended,
                                                    include_now=include_now,
                                                    adjust_type=adjust_type,
                                                    adjust_orig=adjust_orig)
        if convert_to_dataframe:
            df = pd.DataFrame.from_dict(bars)
            if 'datetime' in df.columns:
                df['datetime'] = df['datetime'].map(lambda x: convert_int_to_datetime(x))
                df.set_index('datetime', inplace=True)
                df.index.name = ''
            return df

        return bars


datasource = DataSource()

def is_trading_date(date):
    datasource.is_trading_date(date)

def get_bar(order_book_id, dt, frequency='1d'):
    return datasource.get_bar(order_book_id=order_book_id, dt=dt, frequency=frequency)

def history_bars(
        order_book_id,
        bar_count,
        frequency,
        field,
        dt,
        skip_suspended=True,
        include_now=False,
        adjust_type='pre',
        adjust_orig=None):
    return datasource.history_bars(order_book_id=order_book_id,
                                   bar_count=bar_count,
                                   frequency=frequency,
                                   field=field,
                                   dt=dt,
                                   skip_suspended=skip_suspended,
                                   include_now=include_now,
                                   adjust_type=adjust_type,
                                   adjust_orig=adjust_orig)

def get_bars(order_book_id,
             dt,
             bar_count=1,
             frequency='1d',
             fields=None,
             skip_suspended=True,
             include_now=False,
             adjust_type='pre',
             adjust_orig=None,
             convert_to_dataframe=False):
    return datasource.get_bars(order_book_id=order_book_id,
                               bar_count=bar_count,
                               dt=dt,
                               frequency=frequency,
                               fields=fields,
                               skip_suspended=skip_suspended,
                               include_now=include_now,
                               adjust_type=adjust_type,
                               adjust_orig=adjust_orig,
                               convert_to_dataframe=convert_to_dataframe)

def get_bars_all(order_book_id,
             dt,
             frequency='1d',
             fields=None,
             skip_suspended=True,
             include_now=False,
             adjust_type='pre',
             adjust_orig=None,
             convert_to_dataframe=False):
    return datasource.get_bars_all(order_book_id=order_book_id,
                               dt=dt,
                               frequency=frequency,
                               fields=fields,
                               skip_suspended=skip_suspended,
                               include_now=include_now,
                               adjust_type=adjust_type,
                               adjust_orig=adjust_orig,
                               convert_to_dataframe=convert_to_dataframe)

def get_all_instruments(type=None, date=None):
    """
    获取某个国家市场的所有合约信息。使用者可以通过这一方法很快地对合约信息有一个快速了解，目前仅支持中国市场。

    :param str type: 需要查询合约类型，例如：type='CS'代表股票。默认是所有类型

    :param date: 查询时间点
    :type date: `str` | `datetime` | `date`


    :return: `pandas DataFrame` 所有合约的基本信息。

    其中type参数传入的合约类型和对应的解释如下：

    =========================   ===================================================
    合约类型                      说明
    =========================   ===================================================
    CS                          Common Stock, 即股票
    ETF                         Exchange Traded Fund, 即交易所交易基金
    LOF                         Listed Open-Ended Fund，即上市型开放式基金
    FenjiMu                     Fenji Mu Fund, 即分级母基金
    FenjiA                      Fenji A Fund, 即分级A类基金
    FenjiB                      Fenji B Funds, 即分级B类基金
    INDX                        Index, 即指数
    Future                      Futures，即期货，包含股指、国债和商品期货
    hour                        int - option [1,4]
    minute                      int - option [1,240]
    =========================   ===================================================

    :example:

    获取中国市场所有分级基金的基础信息:

    ..  code-block:: python3
        :linenos:

        [In]all_instruments('FenjiA')
        [Out]
            abbrev_symbol    order_book_id    product    sector_code  symbol
        0    CYGA    150303.XSHE    null    null    华安创业板50A
        1    JY500A    150088.XSHE    null    null    金鹰500A
        2    TD500A    150053.XSHE    null    null    泰达稳健
        3    HS500A    150110.XSHE    null    null    华商500A
        4    QSAJ    150235.XSHE    null    null    鹏华证券A
        ...

    """
    if date is None:
        dt = datetime.datetime.now()
    else:
        dt = pd.Timestamp(date).to_pydatetime()

    if type is not None:
        if isinstance(type, str):
            type = [type]

        types = set()
        for t in type:
            if t == 'Stock':
                types.add('CS')
            elif t == 'Fund':
                types.update(['ETF', 'LOF', 'SF', 'FenjiA', 'FenjiB', 'FenjiMu'])
            else:
                types.add(t)
    else:
        types = None

    result = [i for i in datasource.all_instruments(types, dt)
              if i.type != 'CS' or not datasource.is_suspended(i.order_book_id, dt)]
    if types is not None and len(types) == 1:
        return pd.DataFrame([i.__dict__ for i in result])

    return pd.DataFrame(
        [[i.order_book_id, i.symbol, i.type, i.listed_date, i.de_listed_date] for i in result],
        columns=['order_book_id', 'symbol', 'type', 'listed_date', 'de_listed_date'])

def is_st_stock(book_id, date):
    return datasource.is_st_stock(book_id, date)
