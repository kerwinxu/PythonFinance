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

# TRIX指标的，三重指数平滑移动均线的，买入条件：均线上涨加上收盘价大于sar,卖出条件是止损或者死叉或者收盘价低于sar， 
# 收益平均值:11584.811972000556,方差:8316.240845548848,中位值:9592.800205000005,最大值：195930.68635000003,最小值：1332.7180700000024

class Trix3Strategy(StrategyLog):
    """
    TRIX的交易策略，三重移动均线。
    """
    params = (
        ('trix_period', 14),    # TRIX周期
        ('matrix_period', 9),    # 信号线周期
        ('stop_loss', STOP_LOSS),    # 止损比例 (10%)
        ('af', 0.02),          # 加速因子
    )

    def __init__(self):
        # 计算TRIX指标
        self.trix1 = backtrader.ind.Trix(self.data.close, period=self.params.trix_period)
        # 计算信号线MATRIX（TRIX的移动平均）
        self.matrix = backtrader.ind.SMA(
            self.trix1, period=self.params.matrix_period
        )
        # 金叉死叉信号检测
        self.cross = backtrader.ind.CrossOver(self.trix1, self.matrix)
        # 计算sar
        self.psar = bt.indicators.PSAR(self.data, af=self.params.af)
        # 最后调用父类的
        super().__init__()

    def next(self):
        # 如果已有订单 pending，则不再发新订单
        if self.order:
            return
        # 卖出条件
        sell_conds = [
            self.data.close[0] < self.buyprice * (1 - self.params.stop_loss) if self.buyprice else False,  # 止损条件
            self.cross < 0, # 死叉出现
            self.data.close[0] < self.psar[0]  # 收盘价低于sar
        ]
        # 检查是否持有仓位
        if not self.position and self.matrix[0] > self.matrix[-1] and self.data.close[0] > self.psar[0]:  # 均线上涨且收盘价大于sar
            # **金叉买入**
            self.order = self.order_target_percent(target=0.9) # 每次都0.9个
                # self.order = self.buy()
        elif self.position and any(sell_conds): # 死叉出现且持有仓位时卖出,或者止损线
           self.order = self.close()
                           
if __name__ == '__main__':
    # 仅仅只是做全局的测试
    testStrategy(Trix3Strategy, 
                        file_path=os.path.realpath(__file__), 
                        file_out_name='trix3_止损0.1'
                        )
    
    
  