import pandas as pd
import os


def find_point(df, df_point):

    # df = pd.read_csv(file)
    # if not os.path.exists(target_file):
    #     file_object = open(target_file, 'w+')
    #     list = (
    #             "date" + "," + "key" + ","  + "flag" + ",temp"+"\n")
    #     file_object.writelines(list)
    #     file_object.close()
    # df_point = pd.read_csv(target_file)
    df_point = find(df,df_point)
    # if df_point is not None:
    #     df_point.to_csv(target_file, index=0)
    return df_point


def  find(df, df_point):
    if(len(df) < 4):return
    #初始化
    if (len(df_point) < 2):
        for index in range(3,len(df)-1):

            # a=df.iloc[index]["date"]
            # print(a)
            # if(df.iloc[index]["date"] == '2022-3-3 09:35'):
            #     print("1")

            flag,mark,key =__deal(index, df, df_point)
            if(flag != "no"):
                # print(index)
                new = pd.DataFrame({"date":df.iat[index-1,0],"key":key,"flag":flag,"temp":"yes"},index=[1])
                df_point = df_point.append(new, ignore_index=True)
    #一般情况
    else:
        df_point.drop(df_point[df_point["temp"] == "temp"].index.tolist(), inplace=True)
        i = df[df["date"] == df_point["date"][df_point["temp"] == "yes"].tolist()[0]].index.tolist()[0]
        for index in range(i,len(df)-1):
            flag, mark, key = __deal(index, df, df_point)
            if (flag != "no"):
                new = pd.DataFrame({"date": df.iat[index-1, 0], "key": key, "flag": flag, "temp": "yes"},index=[1])
                df_point = df_point.append(new, ignore_index=True)
    #结束添加临时顶底
    return __deal_temp(df, df_point)



def __deal(index, df, df_point):
    try:
        key,flag = df_point.iloc[-1, 1:3]
    except:
        key=0
        flag=None
    a = df.iloc[index-1]["date"]
    #判断顶点
    if(df.iloc[index-1]["high"]>=df.iloc[index]["high"] and df.iloc[index-1]["high"]>=df.iloc[index-2]["high"]):
        if(flag is  None):
            return "max", index - 1, df.iloc[index - 1]["high"]
        if(flag == "min" and df[df["date"] == df_point.iat[-1, 0]].index.tolist()[0]+3<index):
            df_point.iat[-1, 3] = "no"
            return "max", index - 1, df.iloc[index - 1]["high"]
        #更新顶点
        elif(flag == "max" and key<=df.iloc[index-1]["high"]):
            df_point.drop(df_point.tail(1).index, inplace=True)
            return "max", index - 1, df.iloc[index - 1]["high"]
        else:
            return "no", -1, -1

    elif(df.iloc[index-1]["low"]<=df.iloc[index]["low"] and df.iloc[index-1]["low"]<=df.iloc[index-2]["low"]):
        if (flag is None):
            return "min", index - 1, df.iloc[index - 1]["low"]
        if(flag == "max" and  df[df["date"] == df_point.iat[-1, 0]].index.tolist()[0]+3<index):
            df_point.iat[-1, 3] = "no"
            return "min", index - 1, df.iloc[index - 1]["low"]
        #更新低点
        elif(flag == "min" and key>=df.iloc[index-1]["low"]) :
            df_point.drop(df_point.tail(1).index, inplace=True)
            return "min", index - 1, df.iloc[index - 1]["low"]
        else: return "no", -1, -1
    else:
        return "no", -1, -1

def __deal_temp( df, df_line):
    try:
        #最后一个临时关键点
        index = df[df["date"] == df_line["date"][df_line["temp"] == "yes"].tolist()[0]].index.tolist()[0]
        i = df_line[df_line["temp"] == "yes"].index.tolist()[-1]
        flag = df_line["flag"].iloc[i]
        if(flag == "max"):
            #后面的最低点
            key = df["low"].iloc[index:].min()
            key_index = df[df["low"] == key].index.tolist()[-1]
            new = pd.DataFrame({"date": df["date"].iloc[key_index], "key": key, "flag": "min", "temp": "temp"},index=[1])
            df_line = df_line.append(new, ignore_index=True)
            #寻找是否还有高点
            if(key_index<len(df)-1):
                key = df["high"].iloc[key_index:].max()
                key_index = df[df["high"] == key].index.tolist()[-1]
                new = pd.DataFrame({"date": df["date"].iloc[key_index], "key":key, "flag": "max", "temp": "temp"},index=[1])
                df_line = df_line.append(new, ignore_index=True)
        else:
            # 后面的最高点
            key = df["high"].iloc[index:].max()
            key_index = df[df["high"] == key].index.tolist()[-1]
            new = pd.DataFrame({"date": df["date"].iloc[key_index], "key": key, "flag": "max", "temp": "temp"},index=[1])
            df_line = df_line.append(new, ignore_index=True)
            # 寻找是否还有低点
            if (key_index < len(df)-1):
                key = df["low"].iloc[key_index:].min()
                key_index = df[df["low"] == key].index.tolist()[-1]
                new = pd.DataFrame(
                    {"date": df["date"].iloc[key_index], "key": key, "flag": "min", "temp": "temp"},index=[1])
                df_line = df_line.append(new, ignore_index=True)
                return df_line
        return df_line
    except:
        print("worng:"+str(target_path + file_code))

if __name__ == '__main__':

    path = 'D:\project\data\stock\simple\\5\\'
    target_path = 'D:\project\data\stock\\deal\\5\\'
    file_code = '002627.csv'
    df = pd.read_csv(path + file_code)
    if not os.path.exists(target_path + file_code):
        file_object = open(target_path + file_code, 'w+')
        list = (
                "date" + "," + "key" + ","  + "flag" + ",temp"+"\n")
        file_object.writelines(list)
        file_object.close()
    df_point = pd.read_csv(target_path + file_code)
    df_point = find_point(df, df_point)
    df_point.to_csv(target_path + file_code, index=0)



    # target = ['5']
    # for i in target:
    #     path = 'D:\project\data\stock\simple\\'+i+'\\'
    #     target_path = 'D:\project\data\stock\\deal\\'+i+'\\'
    #     for file_code in os.listdir(path)[0:int((len(os.listdir(path))+1)/2)]:
    #
    #         find_point(path +file_code, target_path + file_code)