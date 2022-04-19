import pandas as pd
import os
import time
import efinance as ef
import yaml
import datetime
from dingtalkchatbot.chatbot import DingtalkChatbot

if __name__ == '__main__':
 # df = ef.stock.get_quote_history(['000001'], klt=5, beg='20220325')
 # for stock_code, df in df.items():
 #  df.drop(axis=1, columns=['股票名称', '股票代码', '振幅', '涨跌幅', '涨跌额', '换手率'], inplace=True)
 #  df.columns = ['date', 'open', 'high', 'low', 'close', 'amount', 'vol']
 #  df[['high', 'low', 'close']] = df[['close', 'high', 'low']]
 #  df[['high', 'close']] = df[['close', 'high']]
 #  df[['high', 'low']] = df[['low', 'high']]
 #
 # a=[1,2,3]
 # print( a[0:len(a)])

 # now = datetime.datetime.now()
 # delta32 = datetime.timedelta(days=32)
 # end = (now - delta32).date().strftime('%Y-%m-%d')
 # print(end)

 # with open('config.yaml') as f:
 #  content = yaml.load(f, Loader=yaml.FullLoader)
 #  f.close()
 #  a= pd.read_csv(content['list_path']+'list.csv',converters={'code': str})['code'].tolist()
 #  print(a)


 a=[1,2,3,4,5]
 s=0
 e=-2
 print( a[e:])
 print( a[s:e])






