import pandas as pd
import os
from utils.regression_tool import stock_macd



def strategy(path,code):

    __data_30 = pd.read_csv(path+'normal\\30\\'+code)
    __data_5 = pd.read_csv(path+'normal\\5\\'+code)
    __data_deal_30 = pd.read_csv(path+'deal\\30\\'+code)
    __data_deal_5 = pd.read_csv(path+'deal\\5\\'+code)
    __data_line_30 = pd.read_csv(path+'line\\30\\'+code)
    __data_line_5 = pd.read_csv(path+'line\\5\\'+code)
    __data_simple_5 = pd.read_csv(path + 'simple\\5\\' + code)
    # __hold = pd.read_csv()
    index = __data_simple_5[__data_simple_5["date"] == __data_line_5.iloc[1]["date"]].index.tolist()[0]
    if index == len(__data_simple_5) -2:
        first_result = first_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5,-1)
        if first_result =='get':
            return
        second_result = second_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5)
        if second_result =='get':
            return
        third_result = third_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5)
        if third_result =='get':
            return

def strategy_test(__data_5,__data_simple_5,__data_deal_5,__data_line_5,__data_30,__data_deal_30,__data_line_30):
    index = __data_simple_5[__data_simple_5["date"] == __data_line_5.iloc[1]["date"]].index.tolist()[0]
    if index == len(__data_simple_5) -2:
        first_result = first_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5,-1)
        # if first_result =='get':
        #     return
        second_result = second_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5)
        # if second_result =='get':
        #     return
        third_result = third_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5)
        #if third_result =='get':
            #return






def first_buying_situation(__data_30,__data_5,__data_deal_30,__data_deal_5,__data_line_30,__data_line_5,index):
    if __data_line_5.iat[-1,0] ==__data_line_30.iat[-1,0]:
        high, low =__volume_case( __data_line_5)
        #找到密集成交区间
        if high!=0 and low!=0:
            flag =0
            #比较最后一段与密集成交前一段力度
            i =index
            now_5_start_index = __data_5[__data_5["date"] == __data_line_5.iloc[i-1]["date"]].index.tolist()[0]
            now_5_end_index = __data_5[__data_5["date"] == __data_line_5.iloc[i]["date"]].index.tolist()[0]
            now_5_macd = __data_5.iloc[now_5_start_index:now_5_end_index + 1]["macd"].sum()
            now_5_dif = __data_5.iloc[now_5_start_index:now_5_end_index + 1]["dif"].max()
            last_5_start_index = __data_5[__data_5["date"] == __data_line_5.iloc[i-5]["date"]].index.tolist()[0]
            last_5_end_index = __data_5[__data_5["date"] == __data_line_5.iloc[i-4]["date"]].index.tolist()[0]
            last_5_macd = __data_5.iloc[last_5_start_index:last_5_end_index + 1]["macd"].sum()
            last_5_dif = __data_5.iloc[last_5_start_index:last_5_end_index + 1]["dif"].max()

            now_30_start_index = __data_30[__data_30["date"] == __data_line_30.iloc[i-1]["date"]].index.tolist()[0]
            now_30_end_index = __data_30[__data_30["date"] == __data_line_30.iloc[i]["date"]].index.tolist()[0]
            now_30_macd = __data_30.iloc[now_30_start_index:now_30_end_index + 1]["macd"].sum()
            now_30_dif = __data_30.iloc[now_30_start_index:now_30_end_index + 1]["dif"].max()
            last_30_start_index = __data_30[__data_30["date"] == __data_line_30.iloc[i-5]["date"]].index.tolist()[0]
            last_30_end_index = __data_30[__data_30["date"] == __data_line_30.iloc[i-4]["date"]].index.tolist()[0]
            last_30_macd = __data_30.iloc[last_30_start_index:last_30_end_index + 1]["macd"].sum()
            last_30_dif = __data_30.iloc[last_30_start_index:last_30_end_index + 1]["dif"].max()

            now_1_end_index =  __data_deal_5[__data_deal_5["date"] ==__data_line_5.iloc[i]["date"]].index.tolist()[0]
            now_1_start_index =  __data_5[__data_5["date"] ==__data_deal_5.iloc[now_1_end_index-1]["date"]].index.tolist()[0]
            now_1_macd = __data_5.iloc[now_1_start_index:now_5_end_index+1]["macd"].sum()
            last_1_start_index = __data_5[__data_5["date"] ==__data_deal_5.iloc[now_1_end_index-3]["date"]].index.tolist()[0]
            last_1_end_index = __data_5[__data_5["date"] ==__data_deal_5.iloc[now_1_end_index-2]["date"]].index.tolist()[0]
            last_1_macd = __data_5.iloc[last_1_start_index:last_1_end_index + 1]["macd"].sum()

            if __data_line_5.iloc["flag"] =="down":
                flag += __deal(now_5_macd,last_5_macd)
                flag += __deal(now_30_macd, last_30_macd)
                flag += __deal(now_30_dif, last_30_dif)
                flag += __deal(now_1_macd, last_1_macd)
                if flag>2:
                    print('first buy :'+code+' '+__data_line_5.iloc[-1]["date"])
                    #return 'get'

def second_buying_situation(__data_30,__data_5,__data_deal_30,__data_deal_5,__data_line_30,__data_line_5):
    if __data_line_5.iat[-1,0] ==__data_line_30.iat[-1,0] and __data_line_5.iat[-1,0] > __data_line_5.iat[-3,0]:
        first_result = first_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5, -3)
        if first_result == 'get':
            now_1_end_index = __data_deal_5[__data_deal_5["date"] == __data_line_5.iloc[-1]["date"]].index.tolist()[0]
            now_5_end_index = __data_5[__data_5["date"] == __data_line_5.iloc[-1]["date"]].index.tolist()[0]
            now_1_start_index = __data_5[__data_5["date"] == __data_deal_5.iloc[now_1_end_index - 1]["date"]].index.tolist()[0]
            now_1_macd = __data_5.iloc[now_1_start_index:now_5_end_index + 1]["macd"].sum()
            last_1_start_index = __data_5[__data_5["date"] == __data_deal_5.iloc[now_1_end_index - 3]["date"]].index.tolist()[0]
            last_1_end_index = __data_5[__data_5["date"] == __data_deal_5.iloc[now_1_end_index - 2]["date"]].index.tolist()[0]
            last_1_macd = __data_5.iloc[last_1_start_index:last_1_end_index + 1]["macd"].sum()
            if __deal(now_1_macd, last_1_macd) ==1:
                print('second buy :' + code + ' ' + __data_line_5.iloc[-1]["date"])
                #return 'get'

def third_buying_situation(__data_30, __data_5, __data_deal_30, __data_deal_5, __data_line_30, __data_line_5):
    if __data_line_5.iat[-1, 0] == __data_line_30.iat[-1, 0]:
        high, low = __volume_case(__data_line_5)
        # 找到密集成交区间
        if high != 0 and low != 0:
            flag = 0
            # 比较最后一段与密集成交前一段力度
            i = -1
            now_5_start_index = __data_5[__data_5["date"] == __data_line_5.iloc[i - 1]["date"]].index.tolist()[0]
            now_5_end_index = __data_5[__data_5["date"] == __data_line_5.iloc[i]["date"]].index.tolist()[0]
            now_5_macd = __data_5.iloc[now_5_start_index:now_5_end_index + 1]["macd"].sum()
            now_5_dif = __data_5.iloc[now_5_start_index:now_5_end_index + 1]["dif"].max()
            last_5_start_index = __data_5[__data_5["date"] == __data_line_5.iloc[i - 5]["date"]].index.tolist()[0]
            last_5_end_index = __data_5[__data_5["date"] == __data_line_5.iloc[i - 4]["date"]].index.tolist()[0]
            last_5_macd = __data_5.iloc[last_5_start_index:last_5_end_index + 1]["macd"].sum()
            last_5_dif = __data_5.iloc[last_5_start_index:last_5_end_index + 1]["dif"].max()

            # now_30_start_index = __data_30[__data_30["date"] == __data_line_30.iloc[i - 1]["date"]].index.tolist()[0]
            # now_30_end_index = __data_30[__data_30["date"] == __data_line_30.iloc[i]["date"]].index.tolist()[0]
            # now_30_macd = __data_30.iloc[now_30_start_index:now_30_end_index + 1]["macd"].sum()
            # now_30_dif = __data_30.iloc[now_30_start_index:now_30_end_index + 1]["dif"].max()
            # last_30_start_index = __data_30[__data_30["date"] == __data_line_30.iloc[i - 5]["date"]].index.tolist()[0]
            # last_30_end_index = __data_30[__data_30["date"] == __data_line_30.iloc[i - 4]["date"]].index.tolist()[0]
            # last_30_macd = __data_30.iloc[last_30_start_index:last_30_end_index + 1]["macd"].sum()
            # last_30_dif = __data_30.iloc[last_30_start_index:last_30_end_index + 1]["dif"].max()

            now_1_end_index = __data_deal_5[__data_deal_5["date"] == __data_line_5.iloc[i]["date"]].index.tolist()[0]
            now_1_start_index = \
            __data_5[__data_5["date"] == __data_deal_5.iloc[now_1_end_index - 1]["date"]].index.tolist()[0]
            now_1_macd = __data_5.iloc[now_1_start_index:now_5_end_index + 1]["macd"].sum()
            last_1_start_index = \
            __data_5[__data_5["date"] == __data_deal_5.iloc[now_1_end_index - 3]["date"]].index.tolist()[0]
            last_1_end_index = \
            __data_5[__data_5["date"] == __data_deal_5.iloc[now_1_end_index - 2]["date"]].index.tolist()[0]
            last_1_macd = __data_5.iloc[last_1_start_index:last_1_end_index + 1]["macd"].sum()

            if __data_line_5.iloc["flag"] == "down":
                flag += __deal(now_5_macd, last_5_macd)
                # flag += __deal(now_30_macd, last_30_macd)
                # flag += __deal(now_30_dif, last_30_dif)
                flag += __deal(now_1_macd, last_1_macd)
                if flag > 0:
                    print('third buy :' + code + ' ' + __data_line_5.iloc[-1]["date"])
                    #return 'get'





def __volume_case(data):
    i=0
    i2 = data.iloc[i-2]["key"]
    i3 = data.iloc[i-3]["key"]
    i4 = data.iloc[i-4]["key"]
    i5 = data.iloc[i-5]["key"]
    if data.iloc[i-2]["flag"] == 'rise':
        if __assess(i2,i5) == "yes":
            high = min(i2, i4)
            low = max(i5, i3)
            return high,low
    else:
        if __assess(i5, i2) == "yes":
            high = min(i5, i3)
            low = max(i2, i4)
            return high, low
    return 0,0


def __assess(high,low):
    if high>low:
        return "yes"
    else:
        return "no"



def __deal(gt,lt):
    if gt>lt:
        return 1


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

    
