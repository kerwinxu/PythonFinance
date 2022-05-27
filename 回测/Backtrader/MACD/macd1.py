# 导入库
from datetime import date, datetime
import backtrader as bt
import pandas as pd
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo
import pandas_datareader as pdr


# 策略类
class TheStrategy(bt.Strategy):
    '''
    This strategy is loosely based on some of the examples from the Van
    K. Tharp book: *Trade Your Way To Financial Freedom*. The logic:

      - Enter the market if:
        - The MACD.macd line crosses the MACD.signal line to the upside
        - The Simple Moving Average has a negative direction in the last x
          periods (actual value below value x periods ago)

     - Set a stop price x times the ATR value away from the close

     - If in the market:

       - Check if the current close has gone below the stop price. If yes,
         exit.
       - If not, update the stop price if the new stop price would be higher
         than the current
    '''

    params = (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('atrperiod', 14),  # ATR Period (standard)
        ('atrdist', 3.0),   # ATR distance for stop price
        ('smaperiod', 30),  # SMA Period (pretty standard)
        ('dirperiod', 10),  # Lookback period to consider SMA trend direction
    )

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def __init__(self):
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)

        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        # To set the stop price
        self.atr = bt.indicators.ATR(self.data, period=self.p.atrperiod)

        # Control market trend
        self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)
        self.smadir = self.sma - self.sma(-self.p.dirperiod)

    def start(self):
        self.order = None  # sentinel to avoid operrations on pending order

    def next(self):
        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market
            if self.mcross[0] > 0.0 and self.smadir < 0.0:
                self.order = self.buy(size=0.1)
                pdist = self.atr[0] * self.p.atrdist
                self.pstop = self.data.close[0] - pdist

        else:  # in the market
            pclose = self.data.close[0]
            pstop = self.pstop

            if pclose < pstop:
                self.close()  # stop met - get out
            else:
                pdist = self.atr[0] * self.p.atrdist
                # Update only if greater than
                self.pstop = max(pstop, pclose - pdist)


if __name__ == "__main__":
    # 要导入的数据
    # start = datetime(2010, 1, 1)
    # end = datetime.now()
    # dt = pd.read_csv("../../../数据获取/baostock/k线数据/sh.600000.csv")
    # # date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST
    # dt.index = pd.to_datetime(dt.date)  # 要有日期
    # dt['openinterest'] = 0             # 这个是期货的。
    # dt = dt[['open', 'high', 'low', 'close', 'volume', 'openinterest']]
    # data0 = bt.feeds.PandasData(dataname=dt, fromdate=start, todate=end)
    data0 = pdr.get_data_fred('GOLDAMGBD228NLBM')
    # data0 = bt.feeds.YahooFinanceData(dataname="AAPL")


    # 回测
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TheStrategy)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    cerebro.broker.setcommission(commission=0.005)  # 佣金 
    cerebro.adddata(data0, name='sh.600000')

    print('初始资金: %.2f' % cerebro.broker.getvalue())
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SharpeRatio')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
    results = cerebro.run()
    strat = results[0]
    print('最终资金: %.2f' % cerebro.broker.getvalue())
    print('夏普比率:', strat.analyzers.SharpeRatio.get_analysis())
    print('回撤指标:', strat.analyzers.DW.get_analysis())
    # b=Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
    # cerebro.plot(b)
    # cerebro.plot(iplot=False)
    # cerebro.plot(style='candlestick')
    cerebro.plot()
