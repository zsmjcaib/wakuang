import pandas as pd
import os
from chart import chart_test
import datetime
import time
from utils.util import read_record
from utils.small_to_large import check, check_second,check_sell
def strategy(content,code):
    demo_path = content['demo_path']

    __data_line_5 = pd.read_csv(content['line_5_path']+code)
    __data_simple_5 = pd.read_csv(content['simple_5_path'] + code)
    __data_5 = pd.read_csv(content['normal_5_path'] + code)
    __data_deal_5 = pd.read_csv(content['deal_5_path'] + code)
    demo_first = read_record(demo_path, code, 'first')
    demo_small = read_record(demo_path, code, 'small')
    demo_second = read_record(demo_path, code, 'second')

    index = __data_simple_5[__data_simple_5["date"] == __data_line_5.iloc[1]["date"]].index.tolist()[0]
    if index == len(__data_simple_5) - 3:
        __data_line_30 = pd.read_csv(content['line_30_path'] + code)
        # 最后不能太无力
        if (__data_simple_5["close"].iloc[-3] <= __data_simple_5["close"].iloc[-1] or __data_simple_5["close"].iloc[-1] >= __data_simple_5["open"].iloc[-3]) \
                and (__data_simple_5["high"].iloc[-1] > __data_simple_5["high"].iloc[-2] or __data_simple_5["close"].iloc[-1] > __data_simple_5["high"].iloc[-3]
                or __data_simple_5["close"].iloc[-1] > (__data_simple_5["high"].iloc[-3] + __data_simple_5["close"].iloc[-3]) / 2) \
                and __data_simple_5.iat[-4, 0] + datetime.timedelta(minutes=-30) <= __data_line_30.iat[-1, 0] <__data_simple_5.iat[-1, 0] + datetime.timedelta(minutes=30):
            __data_30 = pd.read_csv(content['normal_30_path'] + code)
            __data_deal_30 = pd.read_csv(content['deal_30_path'] + code)

            first_result ,mark_price= first_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5,__data_simple_5,-1,code)
            if first_result =='yes':
                demo_first.loc[len(demo_first)] = [__data_5.iat[- 1, 0], mark_price, __data_5.iat[- 1, 2], "", "",
                                                   __data_5.iat[- 2, 2], ""]
                demo_first.to_csv(demo_path + code[:6] + '_first.csv', index=False)


    elif __data_line_5.iloc[-1]["small_to_large"] =='yes' or __data_line_5.iloc[-2]["small_to_large"] =='yes':
            result ,date,mark_price = check(__data_5,__data_line_5)
            if result == 'yes':
                demo_small.loc[len(demo_small)] = [__data_5.iat[- 1, 0], mark_price, __data_5.iat[- 1, 2],"", "", __data_5.iat[- 2, 2], ""]
                demo_small.to_csv(demo_path + code[:6] + '_small.csv', index=False)
                return 'small to buy :' + code +' '+date+' now date'+ str(__data_5.iat[-1,0])
    elif __data_line_5.iat[-1,6] == 'yes' or __data_line_5.iat[-2,6] == 'yes':
            result, date,mark_price = check_second(__data_deal_5, __data_line_5)
            if result == 'yes':
                demo_second.loc[len(demo_second)] = [__data_5.iat[- 1, 0], mark_price,__data_5.iat[- 1, 2], "","", __data_5.iat[- 2, 2], ""]
                demo_second.to_csv(demo_path + code[:6] + '_second.csv', index=False)
                return 'second to buy :' + code + ' ' + date + ' now date ' + str(__data_5.iat[-1, 0])
    elif len(demo_first) > 1 and demo_first.iat[-1, 4] == '':
        return check_sell(demo_first, __data_5, 'first')
    elif len(demo_second) > 1 and demo_second.iat[-1, 4] == '':
        return check_sell(demo_second, __data_5, 'second')
    elif len(demo_small) > 1 and demo_small.iat[-1, 4] == '':
        return check_sell(demo_small, __data_5, 'small')
    return ''
        # second_result = second_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5)
        # if second_result =='yes':
        #     return
        # third_result = third_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5)
        # if third_result =='yes':
        #     return

def strategy_test(__data_5,__data_simple_5,__data_deal_5,__data_line_5,__data_30,__data_deal_30,__data_line_30,code,test_chart_5_path,i,test_chart_30_path,__data_simple_30):
    index = __data_simple_5[__data_simple_5["date"] == __data_line_5.iloc[-1]["date"]].index.tolist()[0]
    if index == len(__data_simple_5) -3:
        #最后不能太无力
        if (__data_simple_5["close"].iloc[-3]<=__data_simple_5["close"].iloc[-1] or __data_simple_5["close"].iloc[-1]>=__data_simple_5["open"].iloc[-3])\
                and  (__data_simple_5["high"].iloc[-1]>__data_simple_5["high"].iloc[-2] or __data_simple_5["close"].iloc[-1]>__data_simple_5["high"].iloc[-3]
                or __data_simple_5["close"].iloc[-1]>(__data_simple_5["high"].iloc[-3]+__data_simple_5["close"].iloc[-3])/2)\
            and __data_simple_5.iat[-4,0]+datetime.timedelta(minutes=-30)<=__data_line_30.iat[-1,0]<__data_simple_5.iat[-1,0]+datetime.timedelta(minutes=30):
            first_result ,mark_price= first_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5,__data_simple_5,-1,code,i)
            return first_result,mark_price
            # if first_result =='yes':
            #     grid_5_chart = chart_test(__data_simple_5, __data_deal_5, __data_line_5)
            #     grid_5_chart.render(test_chart_5_path + code[:6]  + '_'+str(i)+"first.html")
            #     grid_30_chart = chart_test(__data_simple_30, __data_deal_30, __data_line_30)
            #     grid_30_chart.render(test_chart_30_path + code[:6] + '_' + str(i) + "first.html")
            # if first_result == 'no':
            #     grid_5_chart = chart_test(__data_simple_5, __data_deal_5, __data_line_5)
            #     grid_5_chart.render(test_chart_5_path + code[:6]  + '_' + str(i) + "failfirst.html")
            #     grid_30_chart = chart_test(__data_simple_30, __data_deal_30, __data_line_30)
            #     grid_30_chart.render(test_chart_30_path + code[:6] + '_' + str(i) + "failfirst.html")
        #     return
        elif __data_line_5.iat[-1,1]>__data_line_5.iat[-3,1] and __data_line_5["flag"].iloc[-1] =="down":
            if  __data_line_5.iat[-3,4] =='second' or __data_line_5.iat[-3,5] =='yes':
                __data_line_5.iat[-1, 6] = 'yes'
                print(" here: "  +str(__data_line_5.iat[-1, 0]))
    return 'no',0

            # second_result = second_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5,__data_simple_5,code,i)
            # if second_result =='yes':
            #     grid_5_chart = chart_test(__data_simple_5, __data_deal_5, __data_line_5)
            #     grid_5_chart.render(test_chart_5_path + code[:6] + '_' + str(i) + "second.html")
            #     grid_30_chart = chart_test(__data_simple_30, __data_deal_30, __data_line_30)
            #     grid_30_chart.render(test_chart_30_path + code[:6] + '_' + str(i) + "second.html")
            # if second_result == 'no':
            #     grid_5_chart = chart_test(__data_simple_5, __data_deal_5, __data_line_5)
            #     grid_5_chart.render(test_chart_5_path + code[:6] + '_' + str(i) + "failsecond.html")
            #     grid_30_chart = chart_test(__data_simple_30, __data_deal_30, __data_line_30)
            #     grid_30_chart.render(test_chart_30_path + code[:6] + '_' + str(i) + "failsecond.html")
        # third_result = third_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5,code)
        #if third_result =='yes':
            #return






def first_buying_situation(__data_30,__data_5,__data_deal_30,__data_deal_5,__data_line_30,__data_line_5,__data_simple_5,index,code,flag1=''):

    if 1:
        zhigh_5, zlow_5,high_5,low_5 =__volume_case( __data_line_5,index+1)
        # zhigh_30, zlow_30, high_30, low_30 = __volume_case(__data_line_30)
        #找到密集成交区间
        i = index     #-1
        #30分钟起点
        last_30_start_index = measure(__data_line_30,i)
        last_5_start_index = measure(__data_line_5,i)
        #确定下降
        if  __data_line_5.iloc[i]["key"] < low_5 and last_5_start_index != -1 \
                and __data_line_5.iloc[i]["flag"] =="down"  and last_30_start_index != -1 :
            flag =0
            #比较最后一段与密集成交前一段力度
            now_5_end_index = __data_5[__data_5["date"] == __data_line_5.iloc[i]["date"]].index.tolist()[0]
            #判断现在力度是否在减小
            if __data_5.iloc[now_5_end_index]['macd']<=__data_5['macd'].iloc[now_5_end_index+1]<=__data_5['macd'].iloc[now_5_end_index+2]\
                    or __data_5.iloc[now_5_end_index]['macd']>0:
                now_5_start_index = __data_5[__data_5["date"] == __data_line_5["date"].iloc[i-1]].index.tolist()[0]
                df = __data_5.iloc[now_5_start_index:now_5_end_index + 1]
                now_5_macd = df[df['macd'] < 0]['macd'].sum()*1.2
                now_5_macd_min = df['macd'].min()
                df = __data_5.iloc[now_5_start_index:now_5_end_index + 1]
                now_5_diff = df[df['diff'] < 0]["diff"].min()*1.2
                last_5_end_index = __data_5[__data_5["date"] == __data_line_5["date"].iloc[last_5_start_index+1]].index.tolist()[0]
                last_5_start_index = __data_5[__data_5["date"] == __data_line_5["date"].iloc[last_5_start_index]].index.tolist()[0]
                df = __data_5.iloc[last_5_start_index:last_5_end_index + 1]
                last_5_macd = df[df['macd'] < 0]["macd"].sum()
                last_5_macd_min = df['macd'].min()
                df = __data_5.iloc[last_5_start_index:last_5_end_index + 1]
                last_5_diff = df[df['diff'] < 0]["diff"].min()

                now_30_start_index = __data_30[__data_30["date"] == __data_line_30["date"].iloc[i-1]].index.tolist()[0]
                now_30_end_index = __data_30[__data_30["date"] == __data_line_30["date"].iloc[i]].index.tolist()[0]
                df = __data_30.iloc[now_30_start_index:now_30_end_index + 1]
                now_30_macd = df[df['macd'] < 0]["macd"].sum()*1.2
                now_30_macd_min = df['macd'].min()
                df = __data_30.iloc[now_30_start_index:now_30_end_index + 1]
                now_30_diff = df[df['diff'] < 0]["diff"].min()*1.2
                # last_30_start_index = __data_30[__data_30["date"] == __data_line_30.iloc[i-5]["date"]].index.tolist()[0]
                # last_30_end_index = __data_30[__data_30["date"] == __data_line_30.iloc[i-4]["date"]].index.tolist()[0]
                last_30_end_index = __data_30[__data_30["date"] == __data_line_30["date"].iloc[last_30_start_index+1]].index.tolist()[0]
                last_30_start_index = __data_30[__data_30["date"] == __data_line_30["date"].iloc[last_30_start_index]].index.tolist()[0]
                df = __data_30.iloc[last_30_start_index:last_30_end_index + 1]
                last_30_macd = df[df['macd'] < 0]["macd"].sum()
                last_30_macd_min = df['macd'].min()
                df = __data_30.iloc[last_30_start_index:last_30_end_index + 1]
                last_30_diff = df[df['diff'] < 0]["diff"].min()

                now_1_end_index =  __data_deal_5[__data_deal_5["date"] ==__data_line_5["date"].iloc[i]].index.tolist()[0]
                now_1_start_index =  __data_5[__data_5["date"] ==__data_deal_5["date"].iloc[now_1_end_index-1]].index.tolist()[0]
                df = __data_5.iloc[now_1_start_index:now_5_end_index+1]
                now_1_macd = df[df['macd'] < 0]['macd'].sum()*1.2
                now_1_macd_vaule = __data_5.iloc[now_5_end_index+1]['macd']
                last_1_start_index = __data_deal_5[__data_deal_5["date"] == __data_line_5["date"].iloc[i-1]].index.tolist()[0]
                last_1_end_index = now_1_end_index
                last_1 =  __data_deal_5[last_1_start_index:last_1_end_index-1].reset_index()
                last_1_macd = find_last_1_macd(last_1,__data_5,"down")



                if __data_line_5.iloc[-1]["flag"] =="down":
                    str_1 ='5分钟macd不行 '
                    str_2 ='5分钟diff不行 '
                    str_3 ='30分钟macd不行 '
                    str_4 ='30分钟diff不行 '
                    str_5 ='1分钟macd不行 '
                    str_6 = '1分钟macd不背离 '
                    str_7 = '5分钟macd值不行 '
                    str_8 = '30分钟macd值不行 '
                    str_9 = '1分钟macd不背离 '




                    if  __deal(now_5_macd,last_5_macd) == 1:
                        str_1 = '5分钟macd '
                        flag += 1
                    if __deal(now_5_diff, last_5_diff) ==1:
                        str_2 = '5分钟diff '
                        flag += 1
                    if __deal(now_30_macd, last_30_macd)==1:
                        str_3 = '30分钟macd '
                        flag += 1
                    if __deal(now_30_diff, last_30_diff)==1:
                        str_4 = '30分钟diff '
                        flag += 1
                    if __deal(now_1_macd, last_1_macd)==1:
                        str_5 = '1分钟macd '
                        flag += 1
                    if now_1_macd_vaule>0 or now_1_macd_vaule>now_5_macd_min*0.3:
                        flag += 1
                        str_6 = '1分钟macd严重背离 '
                        __data_line_5.iat[-1,4] = 'yes'
                    if now_5_macd_min*1.1>last_5_macd_min:
                        flag += 1
                        str_7 = '5分钟macd值 '
                    if now_30_macd_min * 1.1 > last_30_macd_min:
                        flag += 1
                        str_8 = '30分钟macd值 '
                    if flag>4 and (__deal(now_30_macd, last_30_macd)==1 or __deal(now_30_diff, last_30_diff)==1):
                        # print('first buy :'+code+' '+str(__data_line_5["date"].iloc[-1]) + ' '+str(flag1)+ ' '+str_1+str_2+str_3+str_4+str_5+str_6+str_7+str_8)
                        __data_line_5.iat[-1,5]='yes'
                        return 'yes',__data_line_5["key"].iloc[-1]
                    else:
                        # print('不行' + code + ' ' + str(__data_line_5.iloc[-1]["date"])+ ' '+str(flag1)+ ' '+str_1+str_2+str_3+str_4+str_5+str_6+str_7+str_8)
                        return 'no',0
            else:
                # print('力度没有减小'+code+' '+str(__data_line_5.iloc[-1]["date"]) )
                return 'no',0
        return 'no', 0

def second_first(__data_30,__data_5,__data_deal_30,__data_deal_5,__data_line_30,__data_line_5,__data_simple_5,index,code,flag1):

    if 1:
        zhigh_5, zlow_5,high_5,low_5 =__volume_case( __data_line_5,index+1)
        # zhigh_30, zlow_30, high_30, low_30 = __volume_case(__data_line_30)
        #找到密集成交区间
        i = index     #-1
        #30分钟起点
        last_30_start_index = measure(__data_line_30,-1)
        last_5_start_index = measure(__data_line_5,i)
        #确定下降
        if  __data_line_5.iloc[i]["key"] < low_5 and last_5_start_index != -1 \
                and __data_line_5.iloc[i]["flag"] =="down"  and last_30_start_index != -1 :
            flag =0
            #比较最后一段与密集成交前一段力度
            now_5_end_index = __data_5[__data_5["date"] == __data_line_5.iloc[i]["date"]].index.tolist()[0]
            #判断现在力度是否在减小
            if __data_5.iloc[now_5_end_index]['macd']<=__data_5.iloc[now_5_end_index+1]['macd']<=__data_5.iloc[now_5_end_index+2]['macd']\
                    or __data_5.iloc[now_5_end_index]['macd']>0:
                now_5_start_index = __data_5[__data_5["date"] == __data_line_5.iloc[i-1]["date"]].index.tolist()[0]
                df = __data_5.iloc[now_5_start_index:now_5_end_index + 1]
                now_5_macd = df[df['macd'] < 0]['macd'].sum()*1.2
                now_5_macd_min = df['macd'].min()
                df = __data_5.iloc[now_5_start_index:now_5_end_index + 1]
                now_5_diff = df[df['diff'] < 0]["diff"].min()*1.2
                last_5_end_index = __data_5[__data_5["date"] == __data_line_5.iloc[last_5_start_index+1]["date"]].index.tolist()[0]
                last_5_start_index = __data_5[__data_5["date"] == __data_line_5.iloc[last_5_start_index]["date"]].index.tolist()[0]
                df = __data_5.iloc[last_5_start_index:last_5_end_index + 1]
                last_5_macd = df[df['macd'] < 0]["macd"].sum()
                last_5_macd_min = df['macd'].min()
                df = __data_5.iloc[last_5_start_index:last_5_end_index + 1]
                last_5_diff = df[df['diff'] < 0]["diff"].min()

                now_30_start_index = __data_30[__data_30["date"] == __data_line_30.iloc[i-1]["date"]].index.tolist()[0]
                now_30_end_index = __data_30[__data_30["date"] == __data_line_30.iloc[i]["date"]].index.tolist()[0]
                df = __data_30.iloc[now_30_start_index:now_30_end_index + 1]
                now_30_macd = df[df['macd'] < 0]["macd"].sum()*1.2
                now_30_macd_min = df['macd'].min()
                df = __data_30.iloc[now_30_start_index:now_30_end_index + 1]
                now_30_diff = df[df['diff'] < 0]["diff"].min()*1.2
                # last_30_start_index = __data_30[__data_30["date"] == __data_line_30.iloc[i-5]["date"]].index.tolist()[0]
                # last_30_end_index = __data_30[__data_30["date"] == __data_line_30.iloc[i-4]["date"]].index.tolist()[0]
                last_30_end_index = __data_30[__data_30["date"] == __data_line_30.iloc[last_30_start_index+1]["date"]].index.tolist()[0]
                last_30_start_index = __data_30[__data_30["date"] == __data_line_30.iloc[last_30_start_index]["date"]].index.tolist()[0]
                df = __data_30.iloc[last_30_start_index:last_30_end_index + 1]
                last_30_macd = df[df['macd'] < 0]["macd"].sum()
                last_30_macd_min = df['macd'].min()
                df = __data_30.iloc[last_30_start_index:last_30_end_index + 1]
                last_30_diff = df[df['diff'] < 0]["diff"].min()

                now_1_end_index =  __data_deal_5[__data_deal_5["date"] ==__data_line_5.iloc[i]["date"]].index.tolist()[0]
                now_1_start_index =  __data_5[__data_5["date"] ==__data_deal_5.iloc[now_1_end_index-1]["date"]].index.tolist()[0]
                df = __data_5.iloc[now_1_start_index:now_5_end_index+1]
                now_1_macd = df[df['macd'] < 0]['macd'].sum()*1.2
                now_1_macd_vaule = __data_5.iloc[now_5_end_index+1]['macd']
                last_1_start_index = __data_deal_5[__data_deal_5["date"] == __data_line_5.iloc[i-1]["date"]].index.tolist()[0]
                last_1_end_index = now_1_end_index
                last_1 =  __data_deal_5[last_1_start_index:last_1_end_index-1].reset_index()
                last_1_macd = find_last_1_macd(last_1,__data_5,"down")



                if __data_line_5.iloc[-1]["flag"] =="down":
                    str_1 ='5分钟macd不行 '
                    str_2 ='5分钟diff不行 '
                    str_3 ='30分钟macd不行 '
                    str_4 ='30分钟diff不行 '
                    str_5 ='1分钟macd不行 '
                    str_6 = '1分钟macd不背离 '
                    str_7 = '5分钟macd值不行 '
                    str_8 = '30分钟macd值不行 '
                    str_9 = '1分钟macd不背离 '




                    if  __deal(now_5_macd,last_5_macd) == 1:
                        str_1 = '5分钟macd '
                        flag += 1
                    if __deal(now_5_diff, last_5_diff) ==1:
                        str_2 = '5分钟diff '
                        flag += 1
                    if __deal(now_30_macd, last_30_macd)==1:
                        str_3 = '30分钟macd '
                        flag += 1
                    if __deal(now_30_diff, last_30_diff)==1:
                        str_4 = '30分钟diff '
                        flag += 1
                    if __deal(now_1_macd, last_1_macd)==1:
                        str_5 = '1分钟macd '
                        flag += 1
                    if now_1_macd_vaule>0 or now_1_macd_vaule>now_5_macd_min*0.3:
                        flag += 1
                        str_6 = '1分钟macd严重背离 '
                    if now_5_macd_min*1.1>last_5_macd_min:
                        flag += 1
                        str_7 = '5分钟macd值 '
                    if now_30_macd_min * 1.1 > last_30_macd_min:
                        flag += 1
                        str_8 = '30分钟macd值 '
                    if flag>4 and (__deal(now_30_macd, last_30_macd)==1 or __deal(now_30_diff, last_30_diff)==1):
                        return 'yes'
                    else:
                        return 'no'
            else:
                return 'no'

def second_buying_situation(__data_30,__data_5,__data_deal_30,__data_deal_5,__data_line_30,__data_line_5,__data_simple_5,code,i):
    # first_result = second_first(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5,__data_simple_5, -3,code,i)
    # if first_result == 'yes':
    now_1_end_index = __data_deal_5[__data_deal_5["date"] == __data_line_5.iloc[-1]["date"]].index.tolist()[0]
    now_5_end_index = __data_5[__data_5["date"] == __data_line_5.iloc[-1]["date"]].index.tolist()[0]
    now_1_start_index = __data_5[__data_5["date"] == __data_deal_5.iloc[now_1_end_index - 1]["date"]].index.tolist()[0]
    now_1_macd = __data_5.iloc[now_1_start_index:now_1_end_index + 1]["macd"].sum()

    last_1_start_index = __data_deal_5[__data_deal_5["date"] == __data_line_5.iloc[-1]["date"]].index.tolist()[0]
    last_1 = __data_deal_5[last_1_start_index:now_1_end_index - 1].reset_index()
    last_1_macd = find_last_1_macd(last_1, __data_5, "down")

    if __deal(now_1_macd, last_1_macd) ==1:
        print('second buy :' + code + ' ' + str(__data_line_5.iloc[-1]["date"])+' now '+str(__data_5.iloc[-1]["date"]))
        return 'yes'
    else:
        print('不行 second buy :' + code + ' ' + str(__data_line_5.iloc[-1]["date"])+' now '+str(__data_5.iloc[-1]["date"]))
        return 'no'


def third_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5,code):
    if __data_line_5.iat[-1, 0] == __data_line_30.iat[-1, 0]:
        zhigh, zlow,high,low =__volume_case( __data_line_5)
        # 找到密集成交区间
        if high != 0 and low != 0:
            flag = 0
            # 比较最后一段与密集成交前一段力度
            i = -1
            now_5_start_index = __data_5[__data_5["date"] == __data_line_5.iloc[i - 1]["date"]].index.tolist()[0]
            now_5_end_index = __data_5[__data_5["date"] == __data_line_5.iloc[i]["date"]].index.tolist()[0]
            now_5_macd = __data_5.iloc[now_5_start_index:now_5_end_index + 1]["macd"].sum()
            now_5_diff = __data_5.iloc[now_5_start_index:now_5_end_index + 1]["diff"].max()
            last_5_start_index = __data_5[__data_5["date"] == __data_line_5.iloc[i - 5]["date"]].index.tolist()[0]
            last_5_end_index = __data_5[__data_5["date"] == __data_line_5.iloc[i - 4]["date"]].index.tolist()[0]
            last_5_macd = __data_5.iloc[last_5_start_index:last_5_end_index + 1]["macd"].sum()
            last_5_diff = __data_5.iloc[last_5_start_index:last_5_end_index + 1]["diff"].max()

            # now_30_start_index = __data_30[__data_30["date"] == __data_line_30.iloc[i - 1]["date"]].index.tolist()[0]
            # now_30_end_index = __data_30[__data_30["date"] == __data_line_30.iloc[i]["date"]].index.tolist()[0]
            # now_30_macd = __data_30.iloc[now_30_start_index:now_30_end_index + 1]["macd"].sum()
            # now_30_diff = __data_30.iloc[now_30_start_index:now_30_end_index + 1]["diff"].max()
            # last_30_start_index = __data_30[__data_30["date"] == __data_line_30.iloc[i - 5]["date"]].index.tolist()[0]
            # last_30_end_index = __data_30[__data_30["date"] == __data_line_30.iloc[i - 4]["date"]].index.tolist()[0]
            # last_30_macd = __data_30.iloc[last_30_start_index:last_30_end_index + 1]["macd"].sum()
            # last_30_diff = __data_30.iloc[last_30_start_index:last_30_end_index + 1]["diff"].max()

            now_1_end_index = __data_deal_5[__data_deal_5["date"] == __data_line_5.iloc[i]["date"]].index.tolist()[0]
            now_1_start_index = \
            __data_5[__data_5["date"] == __data_deal_5.iloc[now_1_end_index - 1]["date"]].index.tolist()[0]
            now_1_macd = __data_5.iloc[now_1_start_index:now_5_end_index + 1]["macd"].sum()
            last_1_start_index = \
            __data_5[__data_5["date"] == __data_deal_5.iloc[now_1_end_index - 3]["date"]].index.tolist()[0]
            last_1_end_index = \
            __data_5[__data_5["date"] == __data_deal_5.iloc[now_1_end_index - 2]["date"]].index.tolist()[0]
            last_1_macd = __data_5.iloc[last_1_start_index:last_1_end_index + 1]["macd"].sum()

            if __data_line_5.iloc[-1]["flag"] == "down":
                flag += __deal(now_5_macd, last_5_macd)
                # flag += __deal(now_30_macd, last_30_macd)
                # flag += __deal(now_30_diff, last_30_diff)
                flag += __deal(now_1_macd, last_1_macd)
                if flag > 0:
                    print('third buy :' + code + ' ' + str(__data_line_5.iloc[-1]["date"]))
                    #return 'yes'





def __volume_case(data,i = 0):

    i2 = data["key"].iloc[i-2]
    i3 = data["key"].iloc[i-3]
    i4 = data["key"].iloc[i-4]
    i5 = data["key"].iloc[i-5]
    high = max(i2, i3, i4, i5)
    low = min(i2, i3, i4, i5)
    if data["flag"].iloc[i-2] == 'rise':
        if __assess(i2,i5) == "yes":
            zhigh = min(i2, i4)
            zlow = max(i5, i3)

            return zhigh,zlow,high,low
    else:
        if __assess(i5, i2) == "yes":
            zhigh = min(i5, i3)
            zlow = max(i2, i4)

            return zhigh,zlow,high,low
    return 0,0,high,low


def __assess(high,low):
    if high>low:
        return "yes"
    else:
        return "no"



def __deal(gt,lt):
    if gt>lt:
        return 1
    else:
        return 0

def measure(df,index):
    for i in range(len(df)-2 + index,2,-2):
        #不是最低点
        if df["key"].iloc[i]<df["key"].iloc[-1]:
            return -1
        if df["key"].iloc[i]>df["key"].iloc[-1] and df["key"].iloc[i-1]>df["key"].iloc[-2]:
            return i-1
    return -1

def find_last_1_macd(df,data,flag):
    i = 0
    macd = 0
    temp = 0
    if flag =='down':
        while i<len(df):
            first = data[data["date"] == df["date"].iloc[i]].index.tolist()[0]
            second = data[data["date"] == df["date"].iloc[i+1]].index.tolist()[0]
            new_data = data.iloc[first:second]
            macd = new_data[new_data['macd'] < 0]['macd'].sum()
            if macd >temp:
                macd = temp
            temp = macd
            i += 2
    else:
        while i<len(df):
            first = data[data["date"] == df["date"].iloc[i]].index.tolist()[0]
            second = data[data["date"] == df["date"].iloc[i+1]].index.tolist()[0]
            new_data = data.iloc[first:second]
            macd = new_data[new_data['macd'] > 0]['macd'].sum()
            if macd <temp:
                macd = temp
            temp = macd
            i += 2
    return macd
if __name__ == '__main__':

    path = 'D:\project\data\stock\\'
    line_5_path = 'D:\project\data\stock\line\\5\\'
    line_30_path = 'D:\project\data\stock\line\\30\\'
    deal_5_path = 'D:\project\data\stock\deal\\5\\'
    deal_30_path = 'D:\project\data\stock\deal\\30\\'
    normal_5_path = 'D:\project\data\stock\\normal\\5\\'
    normal_30_path = 'D:\project\data\stock\\normal\\30\\'
    test = 'yes'




    for code in os.listdir(line_5_path)[0:10]:
        strategy(path , code,test)

    # path = 'D:\project\data\stock\\'
    # code ='000001.csv'
    # strategy(path,code)

    
