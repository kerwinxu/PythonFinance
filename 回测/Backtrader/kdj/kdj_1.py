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

# KDJ指标的策略

class KDJ1Strategy(StrategyLog):
    """
    TRIX的交易策略，三重移动均线。
    """
    params = (
        ('period', 9),        # RSV 周期（默认 9）
        ('period_dfast', 3),  # K 的平滑周期（EMA 3）
        ('period_dslow', 3),  # D 的平滑周期（EMA 3）
        # 如下对应kama的参数
        ('kama_period', 10),   # ER 计算窗口（默认10，新手推荐）
        ('fast_period', 2),     # 快速EMA周期（对应SC上限）
        ('slow_period', 30),    # 慢速EMA周期（对应SC下限）
        # 其他参数
        ('stop_loss', STOP_LOSS),    # 止损比例 (10%)
    )

    def __init__(self):
        # 计算kdj指标
        self.kd = bt.indicators.StochasticFull(
            self.data,
            period=self.params.period,
            period_dfast=self.params.period_dfast,
            period_dslow=self.params.period_dslow
        )
        self.K = self.kd.percK
        self.D = self.kd.percDSlow
        self.J = 3 * self.K - 2 * self.D  # 经典定义
        # 自适应均线
        self.kama = bt.indicators.KAMA(
            self.data.close,
            period=self.params.kama_period,
            fast=self.params.fast_period,
            slow=self.params.slow_period
        )
        # 最后调用父类的
        super().__init__()

    def next(self):
        # 如果已有订单 pending，则不再发新订单
        if self.order:
            return
        # 我这里买入条件是k前一日小于20，今天大于20，
        # 卖出条件是多个，止损条件，收盘价低于kama
        sell_conds = [ 
            self.data.close[0] < self.buyprice * (1 - self.params.stop_loss) if self.buyprice else False,  # 止损条件
            self.data.close[0] < self.kama[0]  # 收盘价低于KAMA均线
        ]
        buy_cond = self.K[-1] < 20 and self.K[0] > 20,  # K前一日小于20，今天大于20
        
        if not self.position and buy_cond:
            self.order = self.order_target_percent(target=0.9) # 每次都0.9个
        elif self.position and any(sell_conds): # 有开仓，只要满足卖出条件就卖出
           self.order = self.close()
                           
if __name__ == '__main__': 
    df = testStrategy(KDJ1Strategy, 
                      file_path=os.path.realpath(__file__), 
                      file_out_name='kdj1_止损0.1'
                      )
