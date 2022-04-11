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
    max_list = []
    min_list = []
    ignore_list = []
    df_point = find(df,df_point,max_list,min_list,ignore_list)
    # if df_point is not None:
    #     df_point.to_csv(target_file, index=0)
    return df_point


def  find(df, df_point,max_list,min_list,ignore_list):
    if(len(df) < 4):return
    #初始化
    if (len(df_point) < 2):
        for index in range(3,len(df)):

            # a=df.iloc[index]["date"]
            # print(a)
            # if(df.iloc[index]["date"] == '2022-3-3 09:35'):
            #     print("1")
            if index in ignore_list:
                continue
            flag,mark,key =__deal(index, df, df_point,max_list,min_list,ignore_list)
            if(flag != "no"):
                # print(index)
                new = pd.DataFrame({"date":df.iat[index-1,0],"key":key,"flag":flag,"temp":"yes"},index=[1])
                df_point = df_point.append(new, ignore_index=True)
    #一般情况
    else:
        df_point.drop(df_point[df_point["temp"] == "yes"].index.tolist(), inplace=True)
        i = df[df["date"] == df_point["date"][df_point["temp"] == "no"].tolist()[-1]].index.tolist()[-1]
        for index in range(i,len(df)):
            if index in ignore_list:
                continue
            flag, mark, key = __deal(index, df, df_point,max_list,min_list,ignore_list)
            if (flag != "no"):
                new = pd.DataFrame({"date": df.iat[index-1, 0], "key": key, "flag": flag, "temp": "yes"},index=[1])
                df_point = df_point.append(new, ignore_index=True)
    #结束添加临时顶底
    return __deal_temp(df, df_point,max_list,min_list)



def __deal(index, df, df_point,max_list,min_list,ignore_list):
    try:
        key,flag = df_point.iloc[-1, 1:3]
    except:
        key=0
        flag=None
    if (flag is None):
        if (df.iloc[index - 1]["low"] <= df.iloc[index]["low"] and df.iloc[index - 1]["low"] <= df.iloc[index - 2]["low"]):
            return "min", index - 1, df.iloc[index - 1]["low"]
            # 判断顶点
        elif (df.iloc[index - 1]["high"] >= df.iloc[index]["high"] and df.iloc[index - 1]["high"] >= df.iloc[index - 2]["high"]):
            return "max", index - 1, df.iloc[index - 1]["high"]

        return "no", -1, -1
    last_index = df[df["date"] == df_point.iat[-1, 0]].index.tolist()[0]

    #判断顶点
    if(df.iloc[index-1]["high"]>=df.iloc[index]["high"] and df.iloc[index-1]["high"]>=df.iloc[index-2]["high"]):
        if(flag == "min" and last_index+3<index):
            #更新低点,并忽略前一点
            if min_list !=[]:
                ignore_list.append(last_index)
                df_point.drop(df_point.tail(1).index, inplace=True)
                min_index = min_list.pop(-1)
                return "min", min_index, df.iloc[min_index]["low"]
            #更新顶点前，弹出max_list
            if max_list!=[]:
                max_list.pop()
            df_point.iat[-1, 3] = "no"
            return "max", index - 1, df.iloc[index - 1]["high"]
        #更新顶点
        if(flag == "max" and key<=df.iloc[index-1]["high"]):
            df_point.drop(df_point.tail(1).index, inplace=True)
            if max_list != []:
                max_list.pop()
            if min_list !=[]:
                min_index = min_list.pop(-1)
                df_point.iat[-1,0] = df.iat[min_index,0]
                df_point.iat[-1, 1] = df.iat[min_index, 3]
            return "max", index - 1, df.iloc[index - 1]["high"]
        if flag == "min" and df[df["date"] == df_point.iat[-1, 0]].index.tolist()[0]+3>=index\
                and len(df_point)>2:
            if df.iloc[index-1]["high"]>=df_point.iat[-2,1]:
                max_list.append(index-1)

        # # 更新高点
        # if flag == "min" and df_point.iat[-1, 3] == "yes" and df.iloc[index]["low"]<=df_point.iat[-1, 1] and \
        #         len(df_point)>2 and df_point.iat[-2, 1]<df.iloc[index-1]["high"]:
        #     df_point.drop(df_point.tail(2).index, inplace=True)
        #     return "max", index - 1, df.iloc[index - 1]["high"]

        return "no", -1, -1
    # 判断低点
    elif(df.iloc[index-1]["low"]<=df.iloc[index]["low"] and df.iloc[index-1]["low"]<=df.iloc[index-2]["low"]):

        if(flag == "max" and  last_index+3<index):
            #更新顶点,并忽略前一点
            if max_list !=[]:
                ignore_list.append(last_index)
                df_point.drop(df_point.tail(1).index, inplace=True)
                max_index = max_list.pop(-1)
                return "max", max_index, df.iloc[max_index]["low"]
            #更新低点前，弹出min_list
            if min_list!=[]:
                min_list.pop()
            df_point.iat[-1, 3] = "no"
            return "min", index - 1, df.iloc[index - 1]["low"]
        #更新低点
        if(flag == "min" and key>=df.iloc[index-1]["low"]) :
            df_point.drop(df_point.tail(1).index, inplace=True)
            if min_list != []:
                # min_index = min_list[-1]
                min_list.pop()
            if max_list != []:
                max_index = max_list.pop(-1)
                df_point.iat[-1, 0] = df.iat[max_index, 0]
                df_point.iat[-1, 1] = df.iat[max_index, 2]
            return "min", index - 1, df.iloc[index - 1]["low"]
        #加入不符合条件的更低点
        if flag == "max" and df[df["date"] == df_point.iat[-1, 0]].index.tolist()[0]+3>=index\
            and len(df_point)>2:
            if df.iloc[index-1]["low"]<=df_point.iat[-2,1]:
                min_list.append(index-1)
        # # 更新低点
        # if flag == "max" and df_point.iat[-1, 3] == "yes" and df.iloc[index]["high"]>=df_point.iat[-1, 1]\
        #         and len(df_point)>2 and df_point.iat[-2, 1]>df.iloc[index-1]["low"]:
        #     df_point.drop(df_point.tail(2).index, inplace=True)
        #     return "min", index - 1, df.iloc[index - 1]["low"]
        return "no", -1, -1
    else:
        return "no", -1, -1

def __deal_temp(df, df_point,max_list,min_list):
    try:
        #最后一个临时关键点
        index = df[df["date"] == df_point["date"][df_point["temp"] == "yes"].tolist()[0]].index.tolist()[0]
        i = df_point[df_point["temp"] == "yes"].index.tolist()[-1]
        flag = df_point["flag"].iloc[i]
        if(flag == "max"):
            # #后面的最低点
            # key = df["low"].iloc[index:].min()
            # key_index = df[df["low"] == key].index.tolist()[-1]
            # new = pd.DataFrame({"date": df["date"].iloc[key_index], "key": key, "flag": "min", "temp": "temp"},index=[1])
            # df_line = df_line.append(new, ignore_index=True)
            # #寻找是否还有高点
            # if(key_index<len(df)-1):
            #     key = df["high"].iloc[key_index:].max()
            # 寻找是否还有高点
            if (index < len(df) - 1):
                key = df["high"].iloc[index:].max()
                key_index = df[df["high"] == key].index.tolist()[-1]
                if key>=df_point.iat[-1,1]:
                    df_point.drop(df_point.tail(1).index, inplace=True)
                    if min_list != []:
                        min_index = min_list.pop(-1)
                        df_point.iat[-1, 0] = df.iat[min_index, 0]
                        df_point.iat[-1, 1] = df.iat[min_index, 3]
                    new = pd.DataFrame({"date": df["date"].iloc[key_index], "key":key, "flag": "max", "temp": "yes"},index=[1])
                    df_point = df_point.append(new, ignore_index=True)
                    # 后面的最低点
                    if(key_index<len(df)-1):
                        key  = df["low"].iloc[key_index:].min()
                        key_index = df[df["low"] == key].index.tolist()[-1]
                        new = pd.DataFrame(
                            {"date": df["date"].iloc[key_index], "key": key, "flag": "min", "temp": "yes"}, index=[1])
                        df_point = df_point.append(new, ignore_index=True)


        else:
            # # 后面的最高点
            # key = df["high"].iloc[index:].max()
            # key_index = df[df["high"] == key].index.tolist()[-1]
            # new = pd.DataFrame({"date": df["date"].iloc[key_index], "key": key, "flag": "max", "temp": "temp"},index=[1])
            # df_line = df_line.append(new, ignore_index=True)
            # # 寻找是否还有低点
            # if (key_index < len(df)-1):
            #     key = df["low"].iloc[key_index:].min()
            # 寻找是否还有低点
            if (index < len(df) - 1):
                key = df["low"].iloc[index:].min()
                key_index = df[df["low"] == key].index.tolist()[-1]
                if key<=df_point.iat[-1,1]:
                    df_point.drop(df_point.tail(1).index, inplace=True)
                    if max_list != []:
                        max_index = max_list.pop(-1)
                        df_point.iat[-1, 0] = df.iat[max_index, 0]
                        df_point.iat[-1, 1] = df.iat[max_index, 2]
                    new = pd.DataFrame(
                        {"date": df["date"].iloc[key_index], "key": key, "flag": "min", "temp": "yes"},index=[1])
                    df_point = df_point.append(new, ignore_index=True)
                    # 后面的最高点
                    if (key_index < len(df) - 1):
                        key = df["high"].iloc[key_index:].max()
                        key_index = df[df["high"] == key].index.tolist()[-1]
                        new = pd.DataFrame(
                            {"date": df["date"].iloc[key_index], "key": key, "flag": "max", "temp": "yes"}, index=[1])
                        df_point = df_point.append(new, ignore_index=True)
        return df_point
    except:
        print("worng:"+str(df.iat[-1,0]))

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