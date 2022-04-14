import pandas as pd
import os
from chart import chart_test
import datetime


def strategy_sell(__data_5,__data_simple_5,__data_deal_5,__data_line_5,__data_30,__data_deal_30,__data_line_30,code,test_chart_5_path,i,test_chart_30_path,__data_simple_30):
    index = __data_simple_5[__data_simple_5["date"] == __data_line_5.iloc[-1]["date"]].index.tolist()[0]
    if index == len(__data_simple_5) -3:
        if (__data_simple_5.iloc[-3]["close"]>=__data_simple_5.iloc[-1]["close"] or __data_simple_5.iloc[-1]["close"]<=__data_simple_5.iloc[-3]["open"])\
                and  (__data_simple_5.iloc[-1]["high"]<__data_simple_5.iloc[-2]["high"] or __data_simple_5.iloc[-1]["close"]<__data_simple_5.iloc[-3]["high"]
                or __data_simple_5.iloc[-1]["close"]<(__data_simple_5.iloc[-3]["high"]+__data_simple_5.iloc[-3]["close"])/2)\
            and __data_simple_5.iat[-4,0]+datetime.timedelta(minutes=-30)<=__data_line_30.iat[-1,0]<__data_simple_5.iat[-1,0]+datetime.timedelta(minutes=30):
            first_sell_result = first_selling_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5,__data_simple_5,-1,code,i)
            return first_sell_result

def first_selling_situation(__data_30,__data_5,__data_deal_30,__data_deal_5,__data_line_30,__data_line_5,__data_simple_5,index,code,flag1):
    zhigh_5, zlow_5, high_5, low_5 = __volume_case(__data_line_5, index + 1)
    # zhigh_30, zlow_30, high_30, low_30 = __volume_case(__data_line_30)
    # 找到密集成交区间
    i = index  # -1
    # 30分钟起点
    last_30_start_index = measure(__data_line_30, i)
    last_5_start_index = measure(__data_line_5, i)
    # 确定上升
    if __data_line_5.iloc[i]["key"] > high_5 and last_5_start_index != -1 \
            and __data_line_5.iloc[i]["flag"] == "rise" and last_30_start_index != -1:
        flag = 0
        # 比较最后一段与密集成交前一段力度
        now_5_end_index = __data_5[__data_5["date"] == __data_line_5.iloc[i]["date"]].index.tolist()[0]
        # 判断现在力度是否在减小
        if __data_5.iloc[now_5_end_index]['macd'] >= __data_5.iloc[now_5_end_index + 1]['macd'] >= \
                __data_5.iloc[now_5_end_index + 2]['macd'] \
                or __data_5.iloc[now_5_end_index]['macd'] < 0:
            print("firstsell------------------")
            now_5_start_index = __data_5[__data_5["date"] == __data_line_5.iloc[i - 1]["date"]].index.tolist()[0]
            df = __data_5.iloc[now_5_start_index:now_5_end_index + 1]
            now_5_macd = df[df['macd'] > 0]['macd'].sum() * 1.1
            now_5_macd_max = df['macd'].max()
            df = __data_5.iloc[now_5_start_index:now_5_end_index + 1]
            now_5_diff = df[df['diff'] > 0]["diff"].max() * 1.1
            last_5_end_index = \
            __data_5[__data_5["date"] == __data_line_5.iloc[last_5_start_index + 1]["date"]].index.tolist()[0]
            last_5_start_index = \
            __data_5[__data_5["date"] == __data_line_5.iloc[last_5_start_index]["date"]].index.tolist()[0]
            df = __data_5.iloc[last_5_start_index:last_5_end_index + 1]
            last_5_macd = df[df['macd'] > 0]["macd"].sum()
            last_5_macd_max = df['macd'].max()
            df = __data_5.iloc[last_5_start_index:last_5_end_index + 1]
            last_5_diff = df[df['diff'] > 0]["diff"].max()

            now_30_start_index = __data_30[__data_30["date"] == __data_line_30.iloc[i - 1]["date"]].index.tolist()[0]
            now_30_end_index = __data_30[__data_30["date"] == __data_line_30.iloc[i]["date"]].index.tolist()[0]
            df = __data_30.iloc[now_30_start_index:now_30_end_index + 1]
            now_30_macd = df[df['macd'] > 0]["macd"].sum() * 1.1
            now_30_macd_max = df['macd'].max()
            df = __data_30.iloc[now_30_start_index:now_30_end_index + 1]
            now_30_diff = df[df['diff'] > 0]["diff"].max() * 1.1
            # last_30_start_index = __data_30[__data_30["date"] == __data_line_30.iloc[i-5]["date"]].index.tolist()[0]
            # last_30_end_index = __data_30[__data_30["date"] == __data_line_30.iloc[i-4]["date"]].index.tolist()[0]
            last_30_end_index = \
            __data_30[__data_30["date"] == __data_line_30.iloc[last_30_start_index + 1]["date"]].index.tolist()[0]
            last_30_start_index = \
            __data_30[__data_30["date"] == __data_line_30.iloc[last_30_start_index]["date"]].index.tolist()[0]
            df = __data_30.iloc[last_30_start_index:last_30_end_index + 1]
            last_30_macd = df[df['macd'] > 0]["macd"].sum()
            last_30_macd_max = df['macd'].max()
            df = __data_30.iloc[last_30_start_index:last_30_end_index + 1]
            last_30_diff = df[df['diff'] > 0]["diff"].max()

            now_1_end_index = __data_deal_5[__data_deal_5["date"] == __data_line_5.iloc[i]["date"]].index.tolist()[0]
            now_1_start_index = \
            __data_5[__data_5["date"] == __data_deal_5.iloc[now_1_end_index - 1]["date"]].index.tolist()[0]
            df = __data_5.iloc[now_1_start_index:now_5_end_index + 1]
            now_1_macd = df[df['macd'] > 0]['macd'].sum() * 1.2
            now_1_macd_vaule = __data_5.iloc[now_5_end_index + 1]['macd']
            last_1_start_index = \
            __data_deal_5[__data_deal_5["date"] == __data_line_5.iloc[i - 1]["date"]].index.tolist()[0]
            last_1_end_index = now_1_end_index
            last_1 = __data_deal_5[last_1_start_index:last_1_end_index - 1].reset_index()
            last_1_macd = find_last_1_macd(last_1, __data_5, "rise")



            if __data_line_5.iloc[-1]["flag"] =="rise":
                str_1 ='5分钟macd不行 '
                str_2 ='5分钟diff不行 '
                str_3 ='30分钟macd不行 '
                str_4 ='30分钟diff不行 '
                str_5 ='1分钟macd不行 '
                str_6 = '1分钟macd不背离 '
                str_7 = '5分钟macd值不行 '
                str_8 = '30分钟macd值不行 '
                str_9 = '1分钟macd不背离 '

                if __deal(now_5_macd, last_5_macd) == 1:
                    str_1 = '5分钟macd '
                    flag += 1
                if __deal(now_5_diff, last_5_diff) == 1:
                    str_2 = '5分钟diff '
                    flag += 1
                if __deal(now_30_macd, last_30_macd) == 1:
                    str_3 = '30分钟macd '
                    flag += 1
                if __deal(now_30_diff, last_30_diff) == 1:
                    str_4 = '30分钟diff '
                    flag += 1
                if __deal(now_1_macd, last_1_macd) == 1:
                    str_5 = '1分钟macd '
                    flag += 1
                if now_1_macd_vaule < 0 or now_1_macd_vaule < now_5_macd_max * 0.3:
                    flag += 1
                    str_6 = '1分钟macd严重背离 '
                    __data_line_5.iat[-1, 4] = 'yes'
                if now_5_macd_max * 1.1 < last_5_macd_max:
                    flag += 1
                    str_7 = '5分钟macd值 '
                if now_30_macd_max * 1.1 < last_30_macd_max:
                    flag += 1
                    str_8 = '30分钟macd值 '
                if flag > 4 and (__deal(now_30_macd, last_30_macd) == 1 or __deal(now_30_diff, last_30_diff) == 1):
                    print('first sell :' + code + ' ' + str(__data_line_5.iloc[-1]["date"]) + ' ' + str(
                        flag1) + ' ' + str_1 + str_2 + str_3 + str_4 + str_5 + str_6 + str_7 + str_8)
                    __data_line_5.iat[-1, 5] = 'yes'
                    return 'yes'
                else:
                    print('dont first sell' + code + ' ' + str(__data_line_5.iloc[-1]["date"])+ ' '+str(flag1)+ ' '+str_1+str_2+str_3+str_4+str_5+str_6+str_7+str_8)
                    return 'no'
        else:
            print('力度没有减小'+code+' '+str(__data_line_5.iloc[-1]["date"]) )
            return 'no'

def __volume_case(data,i = 0):

    i2 = data.iloc[i-2]["key"]
    i3 = data.iloc[i-3]["key"]
    i4 = data.iloc[i-4]["key"]
    i5 = data.iloc[i-5]["key"]
    high = max(i2, i3, i4, i5)
    low = min(i2, i3, i4, i5)
    if data.iloc[i-2]["flag"] == 'rise':
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
        if df.iloc[i]["key"]<df.iloc[-1]["key"]:
            return -1
        if df.iloc[i]["key"]>df.iloc[-1]["key"] and df.iloc[i-1]["key"]>df.iloc[-2]["key"]:
            return i-1
    return -1

def find_last_1_macd(df,data,flag):
    i = 0
    macd = 0
    temp = 0
    if flag =='down':
        while i<len(df):
            first = data[data["date"] == df.iloc[i]["date"]].index.tolist()[0]
            second = data[data["date"] == df.iloc[i+1]["date"]].index.tolist()[0]
            new_data = data.iloc[first:second]
            macd = new_data[new_data['macd'] < 0]['macd'].sum()
            if macd >temp:
                macd = temp
            temp = macd
            i += 2
    else:
        while i<len(df):
            first = data[data["date"] == df.iloc[i]["date"]].index.tolist()[0]
            second = data[data["date"] == df.iloc[i+1]["date"]].index.tolist()[0]
            new_data = data.iloc[first:second]
            macd = new_data[new_data['macd'] > 0]['macd'].sum()
            if macd <temp:
                macd = temp
            temp = macd
            i += 2
    return macd