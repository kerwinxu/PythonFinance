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

# TRIX指标的+macd+sar的,3者同时达到买入条件。
# 收益平均值:9967.654700316327,方差:1263.8045591903838,中位值:9739.62705,最大值：21331.417699999998,最小值：6349.601690000001
# 效果很差，很多没有交易。

class Trix4Strategy(StrategyLog):
    """
    TRIX的交易策略，三重移动均线。
    """
    params = (
        ('trix_period', 14),    # TRIX周期
        ('matrix_period', 9),    # 信号线周期
        ('stop_loss', STOP_LOSS),    # 止损比例 (10%)
        ('af', 0.02),          # 加速因子
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
    )

    def __init__(self):
        # 计算TRIX指标
        self.trix1 = backtrader.ind.Trix(self.data.close, period=self.params.trix_period)
        # 计算信号线MATRIX（TRIX的移动平均）
        self.matrix = backtrader.ind.SMA(
            self.trix1, period=self.params.matrix_period
        )
        # 金叉死叉信号检测
        self.trix_cross = backtrader.ind.CrossOver(self.trix1, self.matrix)
        # 计算sar
        self.psar = bt.indicators.PSAR(self.data, af=self.params.af)
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)
        
        # Cross of macd.macd and macd.signal
        self.macd_cross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        # 最后调用父类的
        super().__init__()

    def next(self):
        # 如果已有订单 pending，则不再发新订单
        if self.order:
            return
        # 卖出条件
        sell_conds = [
            self.data.close[0] < self.buyprice * (1 - self.params.stop_loss) if self.buyprice else False,  # 止损条件
            self.trix_cross < 0, # Trix死叉出现
            self.macd_cross < 0, # macd死叉出现
            self.data.close[0] < self.psar[0]  # 收盘价低于sar
        ]
        # 检查是否持有仓位
        if not self.position \
                and self.trix_cross[0] > 0 \
                and self.data.close[0] > self.psar[0] \
                and self.macd_cross[0] > 0:
            # **金叉买入**
            self.order = self.order_target_percent(target=0.9) # 每次都0.9个
                # self.order = self.buy()
        elif self.position and any(sell_conds): # 死叉出现且持有仓位时卖出,或者止损线
           self.order = self.close()
                           
if __name__ == '__main__':
    # 仅仅只是做全局的测试
    testStrategy(Trix4Strategy, 
                        file_path=os.path.realpath(__file__), 
                        file_out_name='trix4_止损0.1'
                        )
    
    
  