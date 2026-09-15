import sys
import os
file_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(file_dir, '../'))
from  trader import testStrategy, StrategyLog
import backtrader

file_dir = os.path.dirname(os.path.realpath(__file__))
file_name = os.path.basename(__file__)
file_name_without_extension = os.path.splitext(file_name)[0]

STOP_LOSS = 0.1

# TRIX指标的，三重指数平滑移动均线的

class DMA1Strategy(StrategyLog):
    """
    DMA,Dickson移动平均线
    """

    params = (
        ('period', 20),        # DMA周期
        ('gainlimit', 50),     # ZeroLag的增益限制
        ('hperiod', 7),        # Hull移动平均线周期
        ('order_pct', 0.95),   # 每次交易使用的资金比例
        ('stop_loss', STOP_LOSS),    # 止损比例 (10%)
    )

    def __init__(self):
        # 初始化DMA指标
        self.dma = backtrader.indicators.DMA(
            self.data.close, 
            period=self.params.period,
            gainlimit=self.params.gainlimit,
            hperiod=self.params.hperiod
        )
        # 金叉死叉信号检测
        self.cross = backtrader.ind.CrossOver(self.data.close, self.dma)
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
    df = testStrategy(DMA1Strategy, 
                      file_path=os.path.realpath(__file__), 
                      file_out_name='Dma止损0.1'
                      )
    # ! 这个平均收益8025，是亏损的