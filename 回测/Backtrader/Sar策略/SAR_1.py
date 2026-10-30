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

# 这个交易策略是分析SAR
# 买入条件收盘价高于sar，卖出条件是止损0.1或者收盘价低于sar,af=0.01，收益平均值:13362.96868049249,方差:13113.923466085273,中位值:10019.380950000006,最大值：245730.2614700002,最小值：1478.8666900000032
# 买入条件收盘价高于sar，卖出条件是止损0.1或者收盘价低于sar,af=0.02，收益平均值:13144.751800311631,方差:12859.478473893463,中位值:9846.26224,最大值：252059.41068,最小值：1580.8628999999985
# 买入条件收盘价高于sar，卖出条件是止损0.1或者收盘价低于sar,af=0.03, 收益平均值:12639.578561227045,方差:11540.930823863908,中位值:9484.00474,最大值：145382.68491000016,最小值：1273.2310600000012


class SAR1Strategy(StrategyLog):
    """
    SAR的交易策略
    """
    params = (
        ('stop_loss', 0.1),    # 止损比例 (10%)
        ('af', 0.02),          # 加速因子
    )
    
    @classmethod
    def introduction(cls):
        return "sar交易策略，收盘价高于sar买入，收盘价低于sar卖出"

    def __init__(self):
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
            # self.data.close[0] < self.buyprice * (1 - self.params.stop_loss) if self.buyprice else False,  # 止损条件
            # self.ma[0] < self.ma[-1],  # 均线降低了
            self.data.close[0] < self.psar[0]  # 收盘价低于sar
        ]
        # 买入条件，收盘价高于sar,
        if not self.position and self.data.close[0] > self.psar[0]:
            # **金叉买入**
            self.order = self.order_target_percent(target=0.9) # 每次都0.9个
        elif self.position and any(sell_conds): # 有开仓，只要满足卖出条件就卖出
            self.order = self.close()

                           
if __name__ == '__main__': 
    df = testStrategy(SAR1Strategy, 
                      file_path=os.path.realpath(__file__), 
                      file_out_name='sar1_止损0.1'
                      )
