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

# KAMA指标的，买入条件：创20日新高,卖出条件kama下跌，收益平均值:8534.024778190424,方差:5758.691281706849,中位值:7269.821539999998,最大值：83763.92240999998,最小值：692.030189999994


class KAMA4Strategy(StrategyLog):
    """
    KAMA的交易策略，自适应均线。
    """
    params = (
        ('kama_period', 10),   # ER 计算窗口（默认10，新手推荐）
        ('fast_period', 2),     # 快速EMA周期（对应SC上限）
        ('slow_period', 30),    # 慢速EMA周期（对应SC下限）
        ('stop_loss', STOP_LOSS),    # 止损比例 (10%)
        ('kama_slope_threshold', 0.05),  # KAMA斜率阈值
        ('af', 0.02),          # 加速因子
    )

    def __init__(self):
        # 计算KAMA指标
        self.kama = bt.indicators.KAMA(
            self.data.close,
            period=self.params.kama_period,
            fast=self.params.fast_period,
            slow=self.params.slow_period
        )
        # 计算sar
        self.psar = bt.indicators.PSAR(self.data, af=self.params.af)
        # 最后调用父类的
        super().__init__()

    def next(self):
        # 如果已有订单 pending，则不再发新订单
        if self.order:
            return
        # 计算KAMA的斜率
        # kama_slope = (self.kama[0] - self.kama[-1]) / self.kama[-1] if self.kama[-1] != 0 else 0
        
        # 卖出条件
        sell_conds = [
            # self.data.close[0] < self.buyprice * (1 - self.params.stop_loss) if self.buyprice else False,  # 止损条件
            # self.data.close[0] < self.kama[0],  # 收盘价低于KAMA均线
            # self.data.close[0] < self.psar[0] , # 收盘价低于sar
            self.kama[0] < self.kama[-1],  # KAMA下跌
        ]
        # 这里求取前面20日新高，
        _highs = []
        for i in range(1, 21):
            _highs.append(self.data.high[-i])

        if not self.position and self.data.close[0] > max(_highs) :  # KAMA上涨且收盘价大于sar
            # **金叉买入**
            self.order = self.order_target_percent(target=0.9) # 每次都0.9个
            # self.order = self.buy()
        elif self.position and any(sell_conds): # 有开仓，只要满足卖出条件就卖出
           self.order = self.close()
                           
if __name__ == '__main__': 
    df = testStrategy(KAMA4Strategy, 
                      file_path=os.path.realpath(__file__), 
                      file_out_name='kama3_止损0.1'
                      )
