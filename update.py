from typing import Dict
import efinance as ef
import pandas as pd
from multiprocessing import Process
from datetime import datetime,timedelta
import yaml
import os
from utils.point import simpleTrend
from  utils.getMacd import stock_macd
from utils.deal import find_point
from utils.line import find_line


def update(stock_codes,content,date = 'all'):
    if date == 'all':
        now = datetime.now()
        delta32 = timedelta(days=32)
        beg = (now - delta32).date().strftime('%Y-%m-%d')
    else:
        beg = datetime.now().date().strftime('%Y-%m-%d')
    for freq in [5,30]:
        # 数据间隔时间为 5 分钟
        total = len(stock_codes)
        each = int(total / 30)
        start = 0
        end = each
        while end<=total+each:
            df_5: Dict[str, pd.DataFrame] = ef.stock.get_quote_history(stock_codes[start:end], klt=freq, beg=beg)
            for stock_code, df in df_5.items():
                if len(df) == 0:
                    continue
                deal(content, df, freq)
            start += each
            end += each

def deal(content,df,freq):
    normal_path = content['normal_'+str(freq)+'_path']
    simple_path = content['simple_'+str(freq)+'_path']
    deal_path = content['deal_'+str(freq)+'_path']
    line_path = content['line_'+str(freq)+'_path']
    code = df.iat[0,1]+'.csv'
    if not os.path.exists(normal_path + code):
        normal = pd.DataFrame(columns=['date','open','high','low','close','amount','vol','diff','dea','macd'])
    else:
        normal = pd.read_csv(normal_path + code)
    df.drop(axis=1, columns=['股票名称', '股票代码','振幅','涨跌幅','涨跌额','换手率'],inplace=True)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'amount', 'vol']
    df[['high', 'close']] = df[['close', 'high']]
    df[['high', 'low']] = df[['low', 'high']]
    df['diff'] = ''
    df['dea'] = ''
    df['macd'] = ''
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    if len(normal)>0:
        normal['date'] = pd.to_datetime(normal['date'], format='%Y-%m-%d')
        #复牌直接加在后面
        try:
            normal_index = df[df['date'] == normal.iat[-2,0]].index.tolist()[-1]
            normal.drop(normal.tail(1).index, inplace=True)
        except:normal_index = 0
        normal = normal.append(df[normal_index+1:],ignore_index=True)
    else:
        normal = df
    normal = macd(normal)
    normal.to_csv(normal_path + code, index=False)
    normal=pd.read_csv(normal_path + code)
    if not os.path.exists(simple_path + code):
        simple = normal.iloc[0:10, 0:7].copy()
    else:
        simple =  pd.read_csv(simple_path + code)
    if not os.path.exists(deal_path + code):
        deal = pd.DataFrame(columns=['date','key','flag','temp'])
    else:
        deal = pd.read_csv(deal_path + code)
    if not os.path.exists(line_path + code):
        line = pd.DataFrame(columns=['date', 'key', 'flag', 'temp','small_to_large','first','second'])
    else:
        line = pd.read_csv(line_path + code)
    try:
        simple = simpleTrend(normal,simple)
        deal = find_point(simple,deal)
        line = find_line(deal,line)
    except:
        print(freq)
        print(code)
    simple.to_csv(simple_path + code, index=False)
    deal.to_csv(deal_path + code, index=False)
    line.to_csv(line_path + code, index=False)

def macd(df) -> pd.DataFrame:
    if len(df)<36:
        return df
    if 'macd' not in df.columns:
        df = stock_macd(df)

        return df
    else:
        df_temp = df[33:]
        index = df_temp[df_temp['macd'] == ''].index.tolist()
        if index!=[]:
            df_normal = df[index[0]-33:]
            df_normal = stock_macd(df_normal)
            df = df[:index[0]].append(df_normal[33:])

        return df

if __name__ == '__main__':
    with open('config.yaml') as f:
        content = yaml.load(f,Loader=yaml.FullLoader)
        f.close()

    df=ef.stock.get_realtime_quotes()
    total = len(df)
    each = int(total / 6)
    p1 = Process(target=update, args=(df.iloc[0:each,0].tolist(),content))
    p2 = Process(target=update, args=(df.iloc[each:2 * each,0].tolist(),content))
    p3 = Process(target=update, args=(df.iloc[2 * each: 3 * each,0].tolist(),content))
    p4 = Process(target=update, args=(df.iloc[3 * each:4 * each,0].tolist(),content ))
    p5 = Process(target=update, args=(df.iloc[4 * each:5 * each,0].tolist(),content ))
    p6 = Process(target=update, args=(df.iloc[5 * each:total+1,0].tolist(),content ))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    # update(df.iloc[0:each,0].tolist(),content)


