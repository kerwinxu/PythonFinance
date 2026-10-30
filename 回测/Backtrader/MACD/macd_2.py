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

# 这个交易策略是分析macd和均线的  
#  收益平均值:10395.485326619366,方差:6189.24288635051,中位值:8935.418269999998,最大值：87820.11707000002,最小值：1581.6894700000028

class MACD2Strategy(StrategyLog):
    """
    TRIX的交易策略，三重移动均线。
    """
    params = (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('stop_loss', STOP_LOSS),    # 止损比例 (10%)
        ('ma_period', 5),      # 均线周期
    )

    def __init__(self):
        # 计算KAMA指标
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)
        # Cross of macd.macd and macd.signal ，macd金叉死叉
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
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
            self.mcross[0] < 0  # macd死叉
        ]
        # 买入条件，1，金叉， 2，均线向上
        if not self.position and self.mcross[0] > 0 and self.ma[0] > self.ma[-1]:
            # **金叉买入**
            self.order = self.order_target_percent(target=0.9) # 每次都0.9个
            # self.order = self.buy()
        elif self.position and any(sell_conds): # 有开仓，只要满足卖出条件就卖出
           self.order = self.close()
                           
if __name__ == '__main__': 
    df = testStrategy(MACD2Strategy, 
                      file_path=os.path.realpath(__file__), 
                      file_out_name='kama2_止损0.1'
                      )
