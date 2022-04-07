import pandas as pd
import os

def simpleTrend(df,df_simple):



    #找第一个新增数据

    tem_data=df[df["date"]>df_simple.iloc[-1]["date"]]
    dfSimple = compare(df_simple,tem_data)
    return dfSimple



def compare(dfSimple,tem_data) -> pd.DataFrame:
    for index,row in tem_data.iterrows():
        dfSimple =calculation(row,dfSimple)
    return dfSimple


def calculation(row,dfSimple) -> pd.DataFrame:
    #右包左
    if(row["high"]>=dfSimple["high"].iloc[-1] and row["low"]<=dfSimple["low"].iloc[-1]):
        dfSimple.iat[-1, 0] = row["date"]
        #上升
        if(dfSimple["high"].iloc[-1]>=dfSimple["high"].iloc[-2]):
            dfSimple.iat[-1, 2] = row["high"]
            #dfSimple.iat[-1, 4] = max(row["close"],dfSimple.at[-1, "low"])
            dfSimple.iat[-1, 4] = max(row["close"],dfSimple.iat[-1, 3])

        #下降
        else:
            dfSimple.iat[-1, 3] = row["low"]
            #dfSimple.iat[-1, 4] = min(row["close"],dfSimple.at[-1, "high"])
            dfSimple.iat[-1, 4] = min(row["close"],dfSimple.iat[-1, 2])

    #左包右
    elif(row["high"]<=dfSimple["high"].iloc[-1] and row["low"]>=dfSimple["low"].iloc[-1]):
        dfSimple.iat[-1, 0] = row["date"]
        #上升
        if(dfSimple["high"].iloc[-1]>=dfSimple["high"].iloc[-2]):
            #dfSimple.iat[-1, 1] = max(row["low"],dfSimple.at[-1, "open"])
            dfSimple.iat[-1, 1] = max(row["low"],dfSimple.iat[-1, 1])
            dfSimple.iat[-1, 3] = row["low"]
        #下降
        else:
            #dfSimple.iat[-1, 1] = min(row["high"],dfSimple.at[-1, "open"])
            dfSimple.iat[-1, 1] = min(row["high"],dfSimple.iat[-1, 1])
            dfSimple.iat[-1, 2] = row["high"]
    else:
        dfSimple = dfSimple.append(row[0:7])
    return dfSimple

if __name__ == '__main__':
    i='5'
    path = 'D:/project/data/stock/normal/' + i + '/'
    target_path = 'D:/project/data/stock/simple/' + i + '/'
    code ='002627.csv'





    df = pd.read_csv(path+code)
    if os.path.exists(target_path+code):
        df_simple = pd.read_csv(target_path+code)
    else:
        df_simple = df.iloc[0:10, 0:7].copy()
    df = simpleTrend(df, df_simple)
    df.to_csv(target_path+code)




