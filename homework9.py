import yfinance as yf
import pandas as pd
from datetime import timedelta
import pyfolio as pf
import matplotlib.pyplot as plt

# 1. 下載台積電2023年股價資料
ticker = yf.Ticker("2330.TW")
data = ticker.history(start="2023-01-01", end="2023-12-31")
data = data[data['Close'] > 0]  # 過濾無效資料

# 2. 移除 index 的時區
data.index = data.index.tz_localize(None)

# 3. 選擇買入日與賣出日
buy_date = pd.to_datetime("2023-07-03")
if buy_date not in data.index:
    buy_date = data.index[data.index.get_indexer([buy_date], method='bfill')[0]]
sell_date = buy_date + timedelta(days=180)
if sell_date not in data.index:
    sell_date = data.index[data.index.get_indexer([sell_date], method='ffill')[0]]

buy_price = data.loc[buy_date, 'Close']
sell_price = data.loc[sell_date, 'Close']

# 4. 計算報酬率序列（每日持有報酬率）
hold_period = data.loc[buy_date:sell_date]
returns = hold_period['Close'].pct_change().fillna(0)

# 5. pyfolio 績效分析
pf.create_simple_tear_sheet(returns)
plt.show()

# 6. 額外資訊
print(f"買入日: {buy_date.date()} 價格: {buy_price:.2f} 元")
print(f"賣出日: {sell_date.date()} 價格: {sell_price:.2f} 元")
print(f"持有180日總報酬率: {(sell_price / buy_price - 1) * 100:.2f}%")
print(f"投入資金: {buy_price * 1000:.0f} 元（1張）")
print(f"賣出資金: {sell_price * 1000:.0f} 元（1張）")
print(f"獲利: {(sell_price - buy_price) * 1000:.0f} 元")
