
from typing import Dict
import efinance as ef
import pandas as pd
import time
from datetime import datetime

def update(code):
    df_5 = ef.stock.get_quote_history(code, klt=5, return_df=1)
    df_30 = ef.stock.get_quote_history(code, klt=30, return_df=1)




    stock_codes = ['000001']
    # 数据间隔时间为 5 分钟
    freq = 5
    status = {stock_code: 0 for stock_code in stock_codes}
    while len(stock_codes) != 0:
        # 获取最新一个交易日的分钟级别股票行情数据
        stocks_df: Dict[str, pd.DataFrame] = ef.stock.get_quote_history(stock_codes, klt=freq)

        for stock_code, df in stocks_df.items():
            # 现在的时间
            now = str(datetime.today()).split('.')[0]
            # 将数据存储到 csv 文件中
            # df.to_csv(f'{stock_code}.csv', encoding='utf-8-sig', index=None)
            if len(df) == status[stock_code]:
                # 移除已经收盘的股票代码
                stock_codes.remove(stock_code)
            status[stock_code] = len(df)

if __name__ == '__main__':
    update('000001')