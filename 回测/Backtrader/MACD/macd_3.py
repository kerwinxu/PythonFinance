import sys
import os
file_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(file_dir, '../'))
from  trader import *
import backtrader

file_dir = os.path.dirname(os.path.realpath(__file__))
file_name = os.path.basename(__file__)
file_name_without_extension = os.path.splitext(file_name)[0]

STOP_LOSS = 0.1

# 这个交易策略是分析macd，
# 买入条件是macd金叉加上昨日macd小于某个阈值-0.2，卖出条件是macd死叉或者止损， 收益平均值:10614.8216096803,方差:3558.435485951453,中位值:9866.718505000003,最大值：43530.28936000002,最小值：2736.30688
# 买入条件是macd金叉加上昨日macd小于某个阈值-0.2，卖出条件是3天后卖出, 收益平均值:10320.611414319887,方差:2489.660306279902,中位值:9958.859350000004,最大值：33889.6875,最小值：3534.73072
# 买入条件是macd金叉加上昨日macd小于某个阈值-0.25，卖出条件是macd死叉或者止损或者均线10下移，收益平均值:10829.899110776241,方差:4148.563292659435,中位值:9956.591499999999,最大值：65305.16336999999,最小值：3330.072750000004
# 买入条件是macd金叉加上昨日macd小于某个阈值-0.25，卖出条件是3天后卖出, 收益平均值:9970.449796699193,方差:2066.6528891446505,中位值:9757.085829999998,最大值：21099.656510000004,最小值：3833.8496099999943

class MACD3Strategy(StrategyLog):
    """
    MACD的交易策略
    """
    params = (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('stop_loss', STOP_LOSS),    # 止损比例 (10%)
        ('ma_period', 20),      # 均线周期
        ('macd_percent_pre_threshold', -0.25), # 昨日macd跟收盘价的比值阈值
    )
    
    @classmethod
    def introduction(cls):
        return "MACD的交易策略, 买入条件是macd金叉加上昨日macd小于某个阈值，卖出条件是macd死叉或者止损"

    def __init__(self):
        # 计算KAMA指标，这里只用到macd的柱状, histo = macd - signal , 也就是macd的差值，macd金叉时，histo>0, macd死叉时，histo<0
        self.macdhist = bt.indicators.MACDHisto(self.data,
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)
        # 这里顺便给出macd的
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)
        # self.macd.macd : macd = ema(data, me1_period) - ema(data, me2_period)
        # self.macd.signal : signal = ema(macd, signal_period)
        
        # 计算均线指标
        self.ma = backtrader.indicators.SimpleMovingAverage(
            self.data.close, 
            period=self.params.ma_period)
        # 买入天数
        self.buy_days = 0
        # 最后调用父类的
        super().__init__()

    def next(self):
        # 如果已有订单 pending，则不再发新订单
        if self.order:
            return

        # 卖出条件
        sell_conds = [
            self.data.close[0] < self.buyprice * (1 - self.params.stop_loss) if self.buyprice else False,  # 止损条件
            # self.ma[0] < self.ma[-1],  # 均线降低了
            self.macdhist[0] < 0  # macd死叉,柱状图小于0就是
        ]
        # 买入条件，1，金叉， 2，昨日macd铜macd的比值小于阈值
        if not self.position and self.macdhist[0] > 0 and self.macdhist[-1]/self.data.close[-1] * 100 < self.params.macd_percent_pre_threshold:
            # **金叉买入**
            self.order = self.order_target_percent(target=0.9) # 每次都0.9个
            self.buy_days = 0
            # self.order = self.buy()
        elif self.position and any(sell_conds): # 有开仓，只要满足卖出条件就卖出
              self.order = self.close()
        # elif self.position:
        #     self.buy_days += 1
        #     if self.buy_days >= 3: # 买入3天后卖出
        #         self.order = self.close()
                           
if __name__ == '__main__': 
    df = testStrategy(MACD3Strategy, 
                      file_path=os.path.realpath(__file__), 
                      file_out_name='macd3_止损0.1'
                      )
