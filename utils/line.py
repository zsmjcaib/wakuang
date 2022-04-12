import pandas as pd
import os


def find_line(df, df_line):


    __find(df, df_line)
    return df_line


def __find(df, df_line):
    if (len(df) < 5): return
    try:
        if df_line.iloc[-1]["small_to_large"] == 'yes':
            small_date = df_line.iloc[-1]["date"]
        else:small_date=''
    except:
        small_date=''
    df_line.drop(df_line[df_line["temp"] == "temp"].index.tolist(), inplace=True)
    df_line.drop(df_line[df_line["temp"] == "yes"].index.tolist(), inplace=True)
    # 初始化
    if (len(df_line) == 0):
        index = -1
        __deal(index, df, df_line)

    else:
        index = df[df["date"] == df_line.iat[-1, 0]].index.tolist()[0]
        __deal(index, df, df_line)
    __last(df, df_line,small_date)


def __deal(index, df, df_line):
    if (len(df_line) == 0):
        i = index
    else:
        i = df[df["date"] == df_line.iat[-1, 0]].index.tolist()[0]
    while i < len(df) - 5:
        # try:
        #     print(df_line.iloc[-1]["date"])
        #     if df_line.iloc[-1]["date"] == '2022-3-11 14:35':
        #     # if i ==135:
        #         print(df_line.iloc[-1]["date"])
        # except: pass
        # 初始化
        try:

            if len(df_line) == 0:
                i+=1
                if df.iloc[i + 1]["key"] > df.iloc[i]["key"]:
                    # 顶点
                    if df.iloc[i + 3]["key"] > df.iloc[i + 1]["key"] and df.iloc[i + 3]["key"] >= df.iloc[i + 5]["key"]:
                        if df.iloc[i + 4]["key"] >= df.iloc[i + 6]["key"]:
                            df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df.iloc[i + 3]["key"], "rise", "no",""]
                            i += 3
                        else:
                            try:
                                flag = df.iloc[i + 6]["key"]
                                j = i + 8
                                while j < len(df) - 1:
                                    if df.iloc[j - 1]["key"] > df.iloc[i + 3]["key"]:
                                        i += 3
                                        break
                                    elif df.iloc[j]["key"] < flag:
                                        df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df.iloc[i + 3]["key"], "rise", "no",""]
                                        i += 3
                                        break
                                    else:i += 1
                            except:
                                return

                elif df.iloc[i + 1]["key"] < df.iloc[i]["key"]:
                    if df.iloc[i + 3]["key"] < df.iloc[i + 1]["key"] and df.iloc[i + 3]["key"] <= df.iloc[i + 5]["key"]:
                        if df.iloc[i + 4]["key"] <= df.iloc[i + 6]["key"]:
                            df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df.iloc[i + 3]["key"], "down", "no",""]
                            i += 3
                        else:
                            try:
                                flag = df.iloc[i + 6]["key"]
                                j = i + 8
                                while j < len(df) - 1:
                                    if (df.iloc[j - 1]["key"] < df.iloc[i + 3]["key"]):
                                        i += 3
                                        break
                                    elif (df.iloc[j]["key"] > flag):
                                        df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df.iloc[i + 3]["key"], "down", "no",""]
                                        i += 3
                                        break
                                    else:i+=1
                            except:
                                return

            else:
                if (df_line.iloc[-1]["flag"] == "down" and df_line.iloc[-1]["temp"] == "no" ) or \
                        df_line.iloc[-1]["flag"] == "rise" and df_line.iloc[-1]["temp"] == "yes" :
                    if (df.iloc[i + 5]["key"] > df.iloc[i + 3]["key"]):
                        i += 2
                        continue
                    # 第一种情况
                    elif (df.iloc[i + 1]["key"] >= df.iloc[i + 4]["key"]):
                        i,result = __first_case(i, df, df_line)
                        if result == "wrong":
                            return
                    elif df.iloc[i + 1]["key"] < df.iloc[i + 4]["key"]:
                        i,result = __second_case(i, df, df_line)
                        if result == "wrong":
                            return

                elif (df_line.iloc[-1]["flag"] == "rise" and df_line.iloc[-1]["temp"] == "no" ) or\
                        df_line.iloc[-1]["flag"] == "down" and df_line.iloc[-1]["temp"] == "yes":
                    if (df.iloc[i + 5]["key"] < df.iloc[i + 3]["key"]):
                        i += 2
                        continue
                    # 第一种情况
                    elif (df.iloc[i + 1]["key"] <= df.iloc[i + 4]["key"]):
                        i,result = __first_case(i, df, df_line)
                        if result == "wrong":
                            return
                    elif (df.iloc[i + 1]["key"] > df.iloc[i + 4]["key"]):
                        i,result = __second_case(i, df, df_line)
                        if result == "wrong":
                            return
                else:
                    i += 2
        except:return


def __first_case(i, df, df_line):
    df_line.drop(df_line[df_line["temp"] == "yes"].index.tolist(), inplace=True)
    if (df_line.iloc[-1]["flag"] == "down"):
        try:
            j = i + 6
            while j < len(df) - 1:
                if (df.iloc[j-1]["key"] > df.iloc[i + 3]["key"]):
                    return i + 4, "no"
                elif (df.iloc[j]["key"] < df.iloc[j - 2]["key"]):
                    df_line.loc[len(df_line)]=[df.iat[i + 3, 0],df.iloc[i + 3]["key"],"rise", "no",""]
                    df_line.loc[len(df_line)]=[df.iat[j, 0],df.iloc[j]["key"],"down", "yes",""]
                    i = df[df["date"] == df_line.iloc[-1]["date"]].index.tolist()[0] - 3
                    return i, "yes"
                j += 2
            return i+2,"out"
        except:
            return 0, "wrong"

    elif (df_line.iloc[-1]["flag"] == "rise"):
        try:
            j = i + 6
            while j < len(df) - 1:
                if (df.iloc[j-1]["key"] < df.iloc[i + 3]["key"]):
                    return i + 4, "no"
                elif (df.iloc[j]["key"] > df.iloc[j - 2]["key"]):
                    df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df.iloc[i + 3]["key"], "down", "no",""]
                    df_line.loc[len(df_line)] = [df.iat[j, 0], df.iloc[j]["key"], "rise", "yes",""]
                    i = df[df["date"] == df_line.iloc[-1]["date"]].index.tolist()[0] - 3
                    return i, "yes"
                j += 2
            return i+2,"out"
        except:
            return 0, "wrong"


def __second_case(i, df, df_line):
    df_line.drop(df_line[df_line["temp"] == "yes"].index.tolist(), inplace=True)
    if (df_line.iloc[-1]["flag"] == "down"):
        index = i + 5
        while index < len(df) :
            if df.iloc[index]["key"] > df.iloc[i + 3]["key"]:
                return i + 4,"no"
            elif df.iloc[index-1]["key"] < df.iloc[i + 4]["key"]:
                df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df.iloc[i + 3]["key"], "rise", "no",""]
                df_line.loc[len(df_line)] = [df.iat[index-1, 0], df.iloc[index-1]["key"], "down", "yes",""]
                i = df[df["date"] == df_line.iloc[-1]["date"]].index.tolist()[0] - 3
                return i,"yes"
            index +=2
        return i + 2, "out"
    elif (df_line.iloc[-1]["flag"] == "rise"):
        index = i + 5
        while index < len(df) :
            if df.iloc[index]["key"] < df.iloc[i + 3]["key"]:
                return i + 4,"no"
            elif df.iloc[index-1]["key"] > df.iloc[i + 4]["key"]:
                df_line.loc[len(df_line)] = [df.iat[i + 3, 0], df.iloc[i + 3]["key"], "down", "no",""]
                df_line.loc[len(df_line)] = [df.iat[index-1, 0], df.iloc[index-1]["key"], "rise", "yes",""]
                i = df[df["date"] == df_line.iloc[-1]["date"]].index.tolist()[0] - 3
                return i,"yes"
            index += 2
        return i + 2, "out"


def  __last(df, df_line,small_date,freq = '5'):
    if len(df_line) == 0 or df[df["date"] == df_line.iat[-1,0]].index.tolist()[0] +3 > len(df):
        return
    else:
        #后面第一个点
        index = df[df["date"] == df_line.iat[-1, 0]].index.tolist()[0]+1
        flag = df_line.iloc[-1]["flag"]
        if flag == "rise":
            #找低点
            key = df["key"].iloc[index:].min()
            key_index = df[df["key"] == key].index.tolist()[-1]
            df_line.loc[len(df_line)] = [df.iat[key_index, 0], key, "down", "temp", ""]
            key_index+=3
            #最后高点
            if (key_index  < len(df)):
                key = df["key"].iloc[key_index:].max()
                #是最高点
                if key == df["key"].iloc[key_index-2:].max():
                    key_index = df[df["key"] == key].index.tolist()[-1]
                    df_line.loc[len(df_line)] = [df.iat[key_index, 0], key, "rise", "temp", ""]
        else:
            # 找高点
            key = df["key"].iloc[index:].max()
            key_index = df[df["key"] == key].index.tolist()[-1]
            df_line.loc[len(df_line)] = [df.iat[key_index, 0], key, "rise", "temp", ""]
            key_index += 3
            # 最后低点
            if (key_index < len(df)):
                key = df["key"].iloc[key_index:].min()
                #是最低点
                if key == df["key"].iloc[key_index-2:].min():
                    key_index = df[df["key"] == key].index.tolist()[-1]
                    df_line.loc[len(df_line)] = [df.iat[key_index, 0], key, "down", "temp", ""]

        # 4月12日前版本
        # while i <len(df):
        #     if df_line.iloc[-1]["flag"] == "rise" :
        #         if df.iloc[i]["key"] >df_line.iloc[-1]["key"]:
        #             #更新高点
        #             df_line.iat[-1,0] = df.iloc[i]["date"]
        #             df_line.iat[-1, 1] = df.iloc[i]["key"]
        #             df_line.iat[-1, 3] = "temp"
        #             index = i
        #
        #         elif i>index+2:
        #             #向下一段
        #             if df.iloc[i]["key"] <df.iloc[index+1]["key"]:
        #                 df_line.loc[len(df_line)] = [df.iat[i, 0], df.iloc[i]["key"], "down", "temp",""]
        #                 index = i
        #
        #         i+=1
        #     elif df_line.iloc[-1]["flag"] == "down" :
        #         if df.iloc[i]["key"] <df_line.iloc[-1]["key"]:
        #             #更新低点
        #             df_line.iat[-1,0] = df.iloc[i]["date"]
        #             df_line.iat[-1, 1] = df.iloc[i]["key"]
        #             df_line.iat[-1, 3] = "temp"
        #             index = i
        #
        #         elif i>index+2:
        #             #向上一段
        #             if df.iloc[i]["key"] >df.iloc[index+1]["key"]:
        #                 df_line.loc[len(df_line)] = [df.iat[i, 0], df.iloc[i]["key"], "rise", "temp",""]
        #                 index = i
        #         i+=1

    if small_date == df_line.iloc[-1]["date"] :
        df_line.iat[-1,4]="yes"
    elif small_date == df_line.iloc[-2]["date"]:
        df_line.iat[-2, 4] = "yes"

if __name__ == '__main__':

    # file="D:\project\data\stock\\deal\\5\\002940.csv"
    # target_file ="D:\project\data\stock\\line\\5\\002940.csv"
    # find_line(file, target_file)
    target = ['5','30']
    for i in target:
        path = 'D:\project\data\stock\\deal\\' + i + '\\'
        target_path = 'D:\project\data\stock\\line\\' + i + '\\'
        for file_code in os.listdir(path):
            if file_code not in os.listdir(target_path):
                df = pd.read_csv(path + file_code)
                if not os.path.exists(target_path+file_code):
                    file_object = open(target_path+file_code, 'w+')
                    list = (
                            "date" + "," + "key" + "," + "flag" + ",temp" + "\n")
                    file_object.writelines(list)
                    file_object.close()
                df_line = pd.read_csv(target_path+file_code)


                find_line(df, df_line)
                df_line.to_csv(target_path +file_code, index=0)
