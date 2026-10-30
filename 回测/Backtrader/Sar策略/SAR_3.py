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

# 这个交易策略是分析SAR，买入条件：收盘价大于sar,k<50，卖出条件：止损加上收盘价低于sar，收益平均值:11429.48146596828,方差:7443.66696569906,中位值:9519.57425499999,最大值：140328.96815999996,最小值：2358.4042999999992
# 这个交易策略是分析SAR，买入条件：收盘价大于sar,d<50，卖出条件：止损加上收盘价低于sar，收益平均值:11829.927221480244,方差:8409.413864382552,中位值:9621.557080000004,最大值：115143.80594999997,最小值：1474.0389999999963
# 这个交易策略是分析SAR，买入条件：收盘价大于sar,j<50，卖出条件：止损加上收盘价低于sar，收益平均值:10700.00105741792,方差:6345.285682167672,中位值:9117.225919999995,最大值：82390.57079000001,最小值：2088.341479999994

class SAR3Strategy(StrategyLog):
    """
    SAR的交易策略
    """
    params = (
        ('stop_loss', 0.1),    # 止损比例 (10%)
        ('af', 0.01),          # 加速因子
        # Standard MACD Parameters
        ('macd1', 12), 
        ('macd2', 26),
        ('macdsig', 9),
        # 均线
        ('ma_period', 20),      # 均线周期
        ("N", 9),              # KDJ周期
        ("m1", 3),             # KDJ平滑参数1
        ("m2", 3),             # KDJ平滑参数2
    )
    
    @classmethod
    def introduction(cls):
        return "sar交易策略，收盘价高于sar买入，收盘价低于sar卖出"
    
    def calu_kdj(self):
        """计算kdj的
        """
        _dataclose = self.datas[0].close
          # 计算交易日内最高价
        _high_s = bt.ind.Highest(self.data.high, period=self.p.N,plot=False)
        _low_s = bt.ind.Lowest(self.data.low, period=self.p.N,plot=False)

        # 计算rsv，未成熟随机值
        _rsv = 100 * bt.DivByZero(
            _dataclose - _low_s
            , _high_s - _low_s
            , zero = None
        )

        # 计算K值
        _K = bt.ind.EMA(_rsv, period = self.p.m1, plot= False)
        _D = bt.ind.EMA(_K, period = self.p.m2, plot = False)
        _J = 3 * _K - 2 * _D
        return (_K, _D, _J)
        

    def __init__(self):
        # 计算sar
        self.psar = bt.indicators.PSAR(self.data, af=self.params.af)
        # 计算KDJ指标
        # self.kdj = bt.indicators.Stochastic(self.data,
        #                                    period=self.p.N,
        #                                    period_dfast=self.p.m1,
        #                                    period_dslow=self.p.m2)
        # # 这里kdj分别是K值和D值
        # self.k = self.kdj.percK
        # self.d = self.kdj.percD
        # 计算kdj
        self.k, self.d, self.j = self.calu_kdj()
        
        # 最后调用父类的
        super().__init__() 

    def next(self):
        # 如果已有订单 pending，则不再发新订单
        if self.order:
            return

        # 卖出条件
        sell_conds = [
            # self.data.close[0] < self.buyprice * (1 - self.params.stop_loss) if self.buyprice else False,  # 止损条件
            # self.ma[0] < self.ma[-1],  # 均线降低了
            self.data.close[0] < self.psar[0]  # 收盘价低于sar
        ]
        # 买入条件，收盘价高于sar,
        if not self.position and self.data.close[0] > self.psar[0]:
            # **金叉买入**
            self.order = self.order_target_percent(target=0.9) # 每次都0.9个
        elif self.position and any(sell_conds): # 有开仓，只要满足卖出条件就卖出
            self.order = self.close()

                           
if __name__ == '__main__': 
    df = testStrategy(SAR3Strategy, 
                      file_path=os.path.realpath(__file__), 
                      file_out_name='sar3_止损0.1'
                      )
