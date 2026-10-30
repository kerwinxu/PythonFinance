import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import periodogram, find_peaks
from numpy.fft import fft, fftfreq

# 看不出来什么

# 这里
import sys
import os
file_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(file_dir, '../../DataSource/聚宽数据'))
import datasource 

codes = datasource.getAStockCodes()
print(f'股票数量:{len(codes)},第一支股票:{codes[0]}')
code = codes[0]
df = datasource.getData(code)

# 假设已获取股票数据 df，含 'close' 列
# --- 1. 数据预处理 ---
log_close = np.log(df['close'].values)
returns = np.diff(log_close)  # 对数收益率序列

# --- 2. 计算功率谱密度（推荐方式）---
fs = 252  # 年交易日数
frequencies, psd = periodogram(
    returns, fs=fs, window='hann', nfft=2048, scaling='density'
)

# --- 3. 识别显著周期 ---
peaks, _ = find_peaks(psd, height=np.percentile(psd, 95))
dominant_periods = fs / frequencies[peaks]  # 单位：交易日
dominant_powers = psd[peaks]

# --- 4. 可视化 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# 频率域
ax1.plot(frequencies[1:], psd[1:])
ax1.set_xlabel('Frequency (1/day)')
ax1.set_ylabel('Power Spectral Density')
ax1.set_title('Frequency Domain')
ax1.grid(True, alpha=0.3)

# 周期域（对数横轴）
ax2.plot(dominant_periods, dominant_powers, 'ro', markersize=6, label='Significant Peaks')
ax2.set_xscale('log')
ax2.set_xlabel('Period (Trading Days)')
ax2.set_ylabel('Power')
ax2.set_title('Dominant Market Cycles')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# --- 5. 输出结果 ---
print("Top 5 Dominant Cycles:")
for i, (T, P) in enumerate(zip(dominant_periods[:5], dominant_powers[:5])):
    print(f"{i+1}. {T:.1f}-day cycle (Power: {P:.2e})")