import pandas as pd

def check(df_deal,df_line):
    if df_line.iloc[-1]["small_to_large"] =='yes' :
        index = df_deal[df_deal["date"]==df_line.iloc[-1]["date"]].index.tolist()[0]
        if len(df_deal)>index+1:
            if df_deal.iloc[index-1]["key"]<df_deal.iloc[index+1]["key"]:
                df_line.iat[-1,4] = 'second'
                return 'yes',str(df_line.iloc[-1]["date"]),df_line.iloc[-1]["key"]
    elif  df_line.iloc[-2]["small_to_large"] =='yes':
        df_line.iat[-2, 4] = 'second'
        return 'yes',str(df_line.iloc[-2]["date"]),df_line.iat[-2,1]
    return 'no','0',0

def check_second(df_deal,df_line):
    if df_line.iat[-1,6] =='yes' and df_deal.iat[-1,2]=='max':
        index = df_deal[df_deal["date"]==df_line.iloc[-1]["date"]].index.tolist()[0]
        if len(df_deal)>index+2:
            # if df_deal.iloc[index-1]["key"]<df_deal.iloc[index+1]["key"]:
            if df_deal.iat[-1,1]>df_deal.iat[-3,1]:
                df_line.iat[-1,6] = ''
                return 'yes',str(df_line.iloc[-1]["date"]),df_line.iloc[-1]["key"]
    elif  df_line.iat[-2,6] =='yes':

        return 'yes',str(df_line.iloc[-2]["date"]),df_line.iat[-2,1]
    return 'no','0',0

def check_sell(df,data,flag):
    #更新高点
    # if df.iloc[-1]['high_price'] ==''or df.iloc[-1]['high_price'] < data.iloc[-1]["high"]:
    #     df.iloc[-1]['high_price'] = data.iloc[-1]["high"]
    if df.iat[-1,5] == '' or df.iat[-1,5] < data.iloc[-1]["high"]:
        df.iat[-1, 5] = data.iloc[-1]["high"]
    if str(df.iat[-1,0])[:10]==  str(data.iat[-1,0])[:10]:
        return
    #强制
    if df.iat[-1,1]>data.iloc[-1]["close"] and df.iat[-1,4]=='':
        df.iat[-1,4] = str(data.iat[-1,0])+'_'+str(data.iloc[-1]["close"])
        df.iat[-1,3] =str(data.iat[-1,0])+'_'+str(data.iloc[-1]["close"])
    #退出等待
    if df.iat[-1, 5] != '':







