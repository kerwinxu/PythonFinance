import sys
import os
file_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(file_dir, '../'))
from  trader import testStrategy, StrategyLog
import backtrader


# 如下是几个常数
SHORT = 5
LONG = 10
STOP_LOSS = 0.05
DAYS = 6
UP_RATE = 1.02

class TenDayMASLStrategy(StrategyLog):
    """
    10日均线交易策略，包含固定百分比止损。
    买入: 收盘价 > 10日均线
    卖出: 1) 收盘价 < 10日均线； 2) 从买入价下跌10%止损
    """
    params = (
        ('short', SHORT),      # 均线周期
        ('long', LONG),      # 均线周期
        ('stop_loss', STOP_LOSS),    # 止损比例 (10%)
        ('days', DAYS),
        ('up_rate', UP_RATE)
    )

    def __init__(self):
        # 初始化简单移动平均线
        self.sma1 = backtrader.ind.SmoothedMovingAverage(self.data, period=self.params.short)
        self.sma2 = backtrader.ind.SmoothedMovingAverage(self.data, period=self.params.long)
        # 初始化止损抛物线
        self.sar = backtrader.ind.ParabolicSAR(self.data)
        # 初始化自适应均线
        self.kama =backtrader.ind.AdaptiveMovingAverage(self.data)
        # 交叉的
        self.cross = backtrader.ind.CrossOver(self.sma1, self.sma2)
        # 用于记录买入订单和买入价格
        self.order = None
        self.buyprice = None
        self.logDebug(f'初始化完毕')

    def next(self):
        # 如果已有订单 pending，则不再发新订单
        if self.order:
            return

        # 检查是否持有仓位
        if not self.position and len(self.data.close) >= self.params.days:
            # **买入条件: 今天的均线大于昨天的百分比**
            if self.kama[0] > self.kama[-1] * self.params.up_rate:
                self.order = self.order_target_percent(target=0.9) # 每次都0.9个
                # self.order = self.buy()
        else:
            # **卖出条件1: 收盘价跌破日均线 (趋势结束)**
            sell_cond1 = self.data.close[0] < self.sma2[0]
            # **卖出条件2: 当前价格较买入价下跌超过止损比例 (风险控制)**
            sell_cond2 = False
            if self.buyprice:
                sell_cond2 = self.data.close[0] < self.buyprice * (1 - self.params.stop_loss)
            # **卖出条件3，均线死叉
            sell_cond3 = self.cross[0] < 0
            # **卖出条件4，止损抛物sar
            sell_cond4 = self.sar[0] > self.data.close[0] 
            # **自适应均线下降超过阈值
            sell_cond5 = self.kama[0] < (1-self.params.stop_loss) * self.kama[-1]
            # !触发任一卖出条件则执行卖出
            sell_conds = [sell_cond1, sell_cond2, sell_cond3, sell_cond4, sell_cond5]
            sell_conds = [i for i in sell_conds if i ]
            if len(sell_conds)>0:
                # reason = '跌破均线' if sell_cond1 else f'触发{self.params.stop_loss*100:.0f}%止损'
                # self.log(f'SELL CREATE ({reason}), Price: {self.data.close[0]:.2f}, Cost: {self.buyprice:.2f}')
                # 卖出全部持仓
                self.order = self.close()


if __name__ == '__main__':
    testStrategy(TenDayMASLStrategy)