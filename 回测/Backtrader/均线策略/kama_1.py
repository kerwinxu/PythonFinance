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

# KAMA指标的，自适应均线,效果很差，资金10000，2000个交易日，平均值才10604.

class KAMA1Strategy(StrategyLog):
    """
    TRIX的交易策略，三重移动均线。
    """
    params = (
        ('kama_period', 10),   # ER 计算窗口（默认10，新手推荐）
        ('fast_period', 2),     # 快速EMA周期（对应SC上限）
        ('slow_period', 30),    # 慢速EMA周期（对应SC下限）
        ('stop_loss', STOP_LOSS),    # 止损比例 (10%)
    )

    def __init__(self):
        # 计算KAMA指标
        self.kama = bt.indicators.KAMA(
            self.data.close,
            period=self.params.kama_period,
            fast=self.params.fast_period,
            slow=self.params.slow_period
        )
        # 可选：添加交叉信号简化逻辑
        self.cross = bt.indicators.CrossOver(self.data.close, self.kama)
        # 最后调用父类的
        super().__init__()

    def next(self):
        # 如果已有订单 pending，则不再发新订单
        if self.order:
            return
        sell_cond2 = False
        if self.buyprice:
            # 判断是否是止损线
            sell_cond2 = self.data.close[0] < self.buyprice * (1 - self.params.stop_loss)
        # 检查是否持有仓位
        if not self.position and self.cross > 0:
            # **金叉买入**
            self.order = self.order_target_percent(target=0.9) # 每次都0.9个
                # self.order = self.buy()
        elif self.position and (self.cross < 0 or sell_cond2): # 死叉出现且持有仓位时卖出,或者止损线
           self.order = self.close()
                           
if __name__ == '__main__':
    df = testStrategy(KAMA1Strategy, 
                      file_path=os.path.realpath(__file__), 
                      file_out_name='kama1_止损0.1'
                      )
