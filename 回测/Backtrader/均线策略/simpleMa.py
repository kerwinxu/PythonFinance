# 导入库
from datetime import date, datetime
import backtrader as bt
import pandas as pd
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo


# 要导入的数据
dt = pd.read_csv("../../../数据获取/baostock/k线数据/sh.600000.csv")
# date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST
dt.index=pd.to_datetime(dt.date) # 要有日期
dt['openinterest']=0             # 这个是期货的。
dt = dt[['open','high','low','close','volume','openinterest']]

# 策略类
class SimpleDoubleMa(bt.SignalStrategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 两个均线
        self.sma1 = bt.ind.SMA(period=5)
        self.sma2 = bt.ind.SMA(period=30)
        # self.sma3 = bt.ind.SMA(period=30)
        self.cross = bt.ind.CrossOver(self.sma1, self.sma2)
    
    def next(self):
        # 我打算这么做，关于买入，
        # 我打算这样做
        if not self.position:
            if self.cross[0] > 0:
                self.buy()
        elif self.cross[0] < 0:
            self.close()

# 回测
cerebro = bt.Cerebro()
cerebro.addstrategy(SimpleDoubleMa)
cerebro.broker.setcommission(commission=0.005) # 佣金
start=datetime(2010, 1, 1)
end=datetime.now()
data0 = bt.feeds.PandasData(dataname=dt,fromdate=start,todate=end)
cerebro.adddata(data0, name='sh.600000')

cerebro.run()
# b=Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
# cerebro.plot(b)
# cerebro.plot(iplot=False)
cerebro.plot(style='candlestick')