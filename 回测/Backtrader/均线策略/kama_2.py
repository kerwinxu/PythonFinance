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

# KAMA指标的，自适应均线,
# 这个版本的，我想要看看斜率，如果斜率够大，那么就可以买入，
# 卖出条件，只要收盘价低于自适应均线或者止损就卖出。
# 效果很差，
# 资金10000，2000个交易日，
# 斜率阈值0.01，平均值才 8658.
# 斜率阈值0.02，平均值才 8189.
# 斜率阈值0.03，平均值才 8076
# 斜率阈值0.04，平均值才 8247
# 斜率阈值0.05，平均值才 8521

class KAMA2Strategy(StrategyLog):
    """
    TRIX的交易策略，三重移动均线。
    """
    params = (
        ('kama_period', 10),   # ER 计算窗口（默认10，新手推荐）
        ('fast_period', 2),     # 快速EMA周期（对应SC上限）
        ('slow_period', 30),    # 慢速EMA周期（对应SC下限）
        ('stop_loss', STOP_LOSS),    # 止损比例 (10%)
        ('kama_slope_threshold', 0.05),  # KAMA斜率阈值
    )

    def __init__(self):
        # 计算KAMA指标
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
        # 计算KAMA的斜率
        kama_slope = (self.kama[0] - self.kama[-1]) / self.kama[-1] if self.kama[-1] != 0 else 0
        
        # 卖出条件
        sell_conds = [
            self.data.close[0] < self.buyprice * (1 - self.params.stop_loss) if self.buyprice else False,  # 止损条件
            self.data.close[0] < self.kama[0]  # 收盘价低于KAMA均线
        ]

        if not self.position and kama_slope > self.params.kama_slope_threshold:
            # **金叉买入**
            self.order = self.order_target_percent(target=0.9) # 每次都0.9个
            # self.order = self.buy()
        elif self.position and any(sell_conds): # 有开仓，只要满足卖出条件就卖出
           self.order = self.close()
                           
if __name__ == '__main__': 
    df = testStrategy(KAMA2Strategy, 
                      file_path=os.path.realpath(__file__), 
                      file_out_name='kama2_止损0.1'
                      )
