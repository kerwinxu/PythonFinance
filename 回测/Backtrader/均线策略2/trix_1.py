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

# TRIX指标的，三重指数平滑移动均线的

class Trix1Strategy(StrategyLog):
    """
    TRIX的交易策略，三重移动均线。
    """
    params = (
        ('trix_period', 14),    # TRIX周期
        ('matrix_period', 9),    # 信号线周期
        ('stop_loss', STOP_LOSS),    # 止损比例 (10%)
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
    print('请选择，1，全股票测试，2，从单个股票选择最优参数，3，所有股票的最优参数')
    order = input().strip()
    if order == '1': 
        df = testStrategy(Trix1Strategy, 
                        file_path=os.path.realpath(__file__), 
                        file_out_name='trix_止损0.1'
                        )
    elif order == '2':
        testStrategyByParams(stratety=Trix1Strategy,code=0, trix_period=[8,10,12,14,16,18,20], matrix_period=[8,10,12,14,16,18,20,22])
    elif order == '3':
        df = testStrategyByParams2(stratety=Trix1Strategy, trix_period=[8,10,12,14,16,18,20], matrix_period=[8,10,12,14,16,18,20,22])
        df.to_csv(os.path.join(file_dir, f'trix_1所有股票最优参数.csv'))