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

# 这个交易策略是分析SAR，再加上macd强势，买入条件是收盘价高于sar，macd强势，卖出条件是止损0.1或者收盘价低于sar或者macd弱势，收益平均值:9532.6222308069,方差:6911.035049338733,中位值:7727.320355000003,最大值：83738.98489,最小值：911.4086899999949
# 买入条件：收盘价高于sar，macd强势，卖出条件是止损0.1或者收盘价低于sar或者macd弱势或者均线降低，收益平均值:9227.234225317194,方差:6785.516866038356,中位值:7512.695969999999,最大值：91850.82216000001,最小值：817.6120699999971
# 买入条件：收盘价高于sar，macd强势，卖出条件是收盘价低于sar,收益平均值:9569.55194287145,方差:6939.635418665338,中位值:7786.374999999999,最大值：87371.27517000001,最小值：879.0713999999933
# 买入条件：收盘价高于sar，均线强势，卖出条件：收盘价低于sar，收益平均值:10807.766014421259,方差:7891.544756640075,中位值:8782.295885,最大值：80926.02365999998,最小值：957.487690000001
# 买入条件：MACD强势，卖出条件：收盘价低于sar或者macd弱势或者止损，收益平均值:7625.908356307735,方差:6086.55705458896,中位值:6054.498334999991,最大值：79255.10896000004,最小值：478.03697000000193

class SAR2Strategy(StrategyLog):
    """
    SAR的交易策略
    """
    params = (
        ('stop_loss', 0.1),    # 止损比例 (10%)
        ('af', 0.02),          # 加速因子
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        # 均线
        ('ma_period', 20),      # 均线周期
    )
    
    @classmethod
    def introduction(cls):
        return "sar交易策略，收盘价高于sar买入，收盘价低于sar卖出"

    def __init__(self):
        # 计算sar
        self.psar = bt.indicators.PSAR(self.data, af=self.params.af)
        # 计算KAMA指标，这里只用到macd的柱状, histo = macd - signal , 也就是macd的差值，macd金叉时，histo>0, macd死叉时，histo<0
        self.macdhist = bt.indicators.MACDHisto(self.data,
                                        period_me1=self.p.macd1,
                                        period_me2=self.p.macd2,
                                        period_signal=self.p.macdsig)
        # 计算均线指标
        self.ma = backtrader.indicators.SimpleMovingAverage(
            self.data.close, 
            period=self.params.ma_period)
        # 最后调用父类的
        super().__init__()

    def next(self):
        # 如果已有订单 pending，则不再发新订单
        if self.order:
            return

        # 卖出条件
        sell_conds = [
            self.data.close[0] < self.buyprice * (1 - self.params.stop_loss) if self.buyprice else False,  # 止损条件
            self.ma[0] < self.ma[-1],  # 均线降低了
            self.data.close[0] < self.psar[0],  # 收盘价低于sar
            self.macdhist[0] < 0  # macd死叉,柱状图小于0就是
        ]
        # 买入条件，收盘价高于sar,macd金叉
        if not self.position and self.data.close[0] > self.psar[0]:
            # **金叉买入**
            self.order = self.order_target_percent(target=0.9) # 每次都0.9个
        elif self.position and any(sell_conds): # 有开仓，只要满足卖出条件就卖出
              self.order = self.close()

                           
if __name__ == '__main__': 
    df = testStrategy(SAR2Strategy, 
                      file_path=os.path.realpath(__file__), 
                      file_out_name='sar2_止损0.1'
                      )
