import pandas as pd

def check(df_deal,df_line):
    if df_line.iloc[-1]["small_to_large"] =='yes' :
        index = df_deal[df_deal["date"]==df_line.iloc[-1]["date"]].index.tolist()[0]
        if len(df_deal)>index+1:
            if df_deal.iloc[index-1]["key"]<df_deal.iloc[index+1]["key"]:
                df_line.iat[-1,4] = ''
                return 'yes',str(df_line.iloc[-1]["date"])
    elif  df_line.iloc[-2]["small_to_large"] =='yes':

        return 'yes',str(df_line.iloc[-2]["date"])
    return 'no','0'