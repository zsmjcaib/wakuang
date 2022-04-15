import pandas as pd
import talib
from chart import chart_test
from utils.point import simpleTrend
from utils.deal import find_point
from utils.line import find_line
from utils.strategy_buy import strategy_test
from utils.small_to_large import check, check_second,check_sell
from utils.util import read_record
from utils.strategy_sell import strategy_sell
import os




def csv_resample(df, rule) -> pd.DataFrame:
    # 重新采样Open列数据
    df_open = round(df['open'].resample(rule=rule, closed='right', label='left').first(), 2)
    df_high = round(df['high'].resample(rule=rule, closed='right', label='left').max(), 2)
    df_low = round(df['low'].resample(rule=rule, closed='right', label='left').min(), 2)
    df_close = round(df['close'].resample(rule=rule, closed='right', label='left').last(), 2)
    df_volume = round(df['vol'].resample(rule=rule, closed='right', label='left').sum(), 2)
    df_amount = round(df['amount'].resample(rule=rule, closed='right', label='left').sum(), 2)
    # print("新周期数据已生成")
    # 生成新周期数据
    df_15t = pd.DataFrame()
    df_15t = df_15t.assign(open=df_open)
    df_15t = df_15t.assign(high=df_high)
    df_15t = df_15t.assign(low=df_low)
    df_15t = df_15t.assign(close=df_close)
    df_15t = df_15t.assign(amount=df_amount)
    df_15t = df_15t.assign(vol=df_volume)
    # 去除空值
    df_15t = df_15t.dropna()

    return df_15t

# 读取csv文件，返回pd.DataFrame对象
def import_csv(df,rule) -> pd.DataFrame:

    df =df.copy()
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df = df.set_index(['date'])
    df = csv_resample(df, rule)
    df.reset_index(inplace=True)
    return df


def macd(df):
    diff, dea, macd = talib.MACD(df["close"],
                                 fastperiod=12,
                                 slowperiod=26,
                                 signalperiod=9)
    df["diff"] = round(diff, 2)
    df["dea"] = round(dea, 2)
    df["macd"] = round(macd * 2, 2)
    return df


def stock_macd(df) -> pd.DataFrame:
    if len(df)<36:
        return df
    if 'macd' not in df.columns:
        df = macd(df)
        return df
    else:
        df_temp = df[33:]
        index = df_temp[df_temp['macd'] == ''].index.tolist()
        if index!=[]:
            df_normal = df[index[0]-33:]
            df_normal = macd(df_normal)
            df = df[:index[0]-33].append(df_normal)

        return df


def test(path,code,content):
    real_data = pd.read_csv(path + code)
    test_normal_5_path = content['test_normal_5_path']
    test_normal_30_path = content['test_normal_30_path']
    test_simple_5_path = content['test_simple_5_path']
    test_simple_30_path = content['test_simple_30_path']
    test_deal_5_path = content['test_deal_5_path']
    test_deal_30_path = content['test_deal_30_path']
    test_line_5_path = content['test_line_5_path']
    test_line_30_path = content['test_line_30_path']
    test_chart_5_path = content['test_chart_5_path']
    test_chart_30_path = content['test_chart_30_path']
    demo_path = content['demo_path']
    test_5 = real_data[0:5000]
    #初始化
    test_30 = import_csv(test_5,'30T')
    test_5_simple = test_5.iloc[0:10, 0:7].copy()
    test_30_simple = test_30.iloc[0:10, 0:7].copy()
    if not os.path.exists(test_deal_5_path + code):
        test_5_deal = pd.DataFrame(columns=['date','key','flag','temp'])
        test_30_deal = pd.DataFrame(columns=['date','key','flag','temp'])
        test_5_line = pd.DataFrame(columns=['date', 'key', 'flag', 'temp','small_to_large','first','second'])
        test_30_line = pd.DataFrame(columns=['date', 'key', 'flag', 'temp','small_to_large','first','second'])
    else:
        test_5_deal = pd.read_csv(test_deal_5_path + code)
        test_30_deal = pd.read_csv(test_deal_30_path + code)
        test_5_line = pd.read_csv(test_deal_5_path + code)
        test_30_line = pd.read_csv(test_deal_30_path + code)
    demo_first = read_record(demo_path,code,'first')
    demo_second = read_record(demo_path,code,'second')
    demo_small = read_record(demo_path,code,'small')

    test_5 = stock_macd(test_5)
    test_30 = stock_macd(test_30)
    #开始回测
    for i, row in real_data[5000:].iterrows():

        test_5 = test_5.append(row)
        test_5 = stock_macd(test_5)
        test_30 = import_csv(test_5, '30T')
        test_30 = stock_macd(test_30)
        test_5_simple =simpleTrend(test_5,test_5_simple)
        test_30_simple =simpleTrend(test_30,test_30_simple)
        test_5_simple.reset_index(drop=True, inplace=True)
        test_30_simple.reset_index(drop=True, inplace=True)
        test_5_deal = find_point(test_5_simple, test_5_deal)
        test_30_deal = find_point(test_30_simple, test_30_deal)
        test_5_line = find_line(test_5_deal , test_5_line)
        test_30_line = find_line(test_30_deal , test_30_line)
        if str(test_5.iloc[-1]["date"]) == '2022-02-22 10:10:00':
            print(1)

            # grid_5_chart = chart_test(test_5_simple, test_5_deal, test_5_line)
            # grid_5_chart.render(test_chart_5_path + code[:6] + '_' + str(i) + ".html")
        #     2022-02-17 13:20:00
        if i ==5000:
            print(i)
        # print(i)
        # print(str(i)+' '+str(test_5_line.iat[-1,0])+' '+str(test_5_line.iat[-2,0])+' '+str(test_5_line.iat[-3,0]))
        result,mark_price = strategy_test(test_5,test_5_simple,test_5_deal,test_5_line,test_30,test_30_deal,test_30_line,code[:6],test_chart_5_path,i,test_chart_30_path,test_30_simple)
        if  result == 'yes':
            demo_first.loc[len(demo_first)] = [test_5.iat[- 1, 0], mark_price,test_5.iat[- 1, 2],"", "", test_5.iat[- 2, 2], ""]
        if test_5_line.iloc[-1]["small_to_large"] =='yes' or test_5_line.iloc[-2]["small_to_large"] =='yes':
            result ,date,mark_price = check(test_5_deal,test_5_line)
            if result == 'yes':
                demo_small.loc[len(demo_small)] = [test_5.iat[- 1, 0], mark_price, test_5.iat[- 1, 2],"", "", test_5.iat[- 2, 2], ""]
                print('small to buy :' + code + ' '+str(i) + ' '+date+' now date'+ str(test_5.iat[-1,0]))
            # elif result == 'no':
            #     print('small to buy fail :' + code + ' '+str(i) + ' '+ str(test_5_line.iloc[-1]["date"]))

        if test_5_line.iat[-1,6] == 'yes' or test_5_line.iat[-2,6] == 'yes':
            result, date,mark_price = check_second(test_5_deal, test_5_line)
            if result == 'yes':
                demo_second.loc[len(demo_second)] = [test_5.iat[- 1, 0], mark_price,test_5.iat[- 1, 2], "","", test_5.iat[- 2, 2], ""]

                print('second to buy :' + code + ' ' + str(i) + ' ' + date + ' now date ' + str(test_5.iat[-1, 0]))
            # elif result == 'no':
                # print('second to buy fail :' + code + ' '+str(i) + ' '+ str(test_5_line.iloc[-1]["date"])+ ' now date ' + str(test_5.iat[-1, 0]))

        result = strategy_sell(test_5,test_5_simple,test_5_deal,test_5_line,test_30,test_30_deal,test_30_line,code[:6],test_chart_5_path,i,test_chart_30_path,test_30_simple)






        #止损
        if len(demo_first)>1 and demo_first.iat[-1,4]=='':
            check_sell(demo_first,test_5,'first')
        if len(demo_second) > 1 and demo_second.iat[-1, 4] == '':
            check_sell(demo_second, test_5,'second')
        if len(demo_small) > 1 and demo_small.iat[-1, 4] == '':
            check_sell(demo_small, test_5,'small')


        if i%1000 ==0:
            # test_5.to_csv(test_normal_5_path+code[:6]+'_'+str(i) +'.csv')
            # test_30.to_csv(test_normal_30_path+code[:6]+'_'+str(i) +'.csv')
            # test_5_simple.to_csv(test_simple_5_path+code[:6]+'_'+str(i) +'.csv')
            # test_30_simple.to_csv(test_simple_30_path+code[:6]+'_'+str(i) +'.csv')
            # test_5_deal.to_csv(test_deal_5_path+code[:6]+'_'+str(i) +'.csv')
            # test_30_deal.to_csv(test_deal_30_path+code[:6]+'_'+str(i) +'.csv')
            # test_5_line.to_csv(test_line_5_path+code[:6]+'_'+str(i) +'.csv')
            # test_30_line.to_csv(test_line_30_path+code[:6]+'_'+str(i) +'.csv')
            grid_5_chart = chart_test(test_5_simple,test_5_deal,test_5_line)
            grid_5_chart.render(test_chart_5_path+code[:6]+'_'+str(i) + ".html")
            grid_30_chart = chart_test(test_30_simple, test_30_deal, test_30_line)
            grid_30_chart.render(test_chart_30_path + code[:6] + '_' + str(i) + ".html")
    grid_5_chart = chart_test(test_5_simple, test_5_deal, test_5_line)
    grid_5_chart.render(test_chart_5_path + code[:6] + '_' + 'last' + ".html")
    grid_30_chart = chart_test(test_30_simple, test_30_deal, test_30_line)
    grid_30_chart.render(test_chart_30_path + code[:6] + '_' + 'last' + ".html")
    demo_first.to_csv(demo_path+code[:6] +'_first.csv')
    demo_small.to_csv(demo_path + code[:6] + '_small.csv')
    demo_second.to_csv(demo_path + code[:6] + '_second.csv')



