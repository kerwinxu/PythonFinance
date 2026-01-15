from datetime import datetime
import backtrader as bt
import pandas as pd
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        self.crossover = bt.ind.CrossOver(sma1, sma2)
        # self.signal_add(bt.SIGNAL_LONG, crossover)
    
    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()


cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)
cerebro.broker.setcommission(commission=0.01) # 佣金1%

# 这里导入一个数据
dt = pd.read_csv("../../../数据获取/baostock/k线数据/sh.600000.csv")
# date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST
dt.index=pd.to_datetime(dt.date) # 要有日期
dt['openinterest']=0             # 这个是期货的。
dt = dt[['open','high','low','close','volume','openinterest']]



# data0 = bt.feeds.YahooFinanceData(dataname='MSFT', fromdate=datetime(2020, 1, 1),
#                                   todate=datetime(2020, 12, 31))



start=datetime(2015, 1, 1)
end=datetime(2021, 10, 22)
data0 = bt.feeds.PandasData(dataname=dt,fromdate=start,todate=end)
cerebro.adddata(data0, name='sh.600000')

cerebro.run()
# b=Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
# cerebro.plot(b)
cerebro.plot(iplot=False)