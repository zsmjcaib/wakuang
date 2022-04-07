import pandas as pd
import os
if __name__ == '__main__':
    path = 'D:/project/data/stock/normal/30/000001.csv'
    df = pd.read_csv(path)
    df_line = pd.DataFrame
    i='5'
    path = 'D:/project/data/stock/normal/' + i + '/'
    target_path = 'D:/project/data/stock/simple/' + i + '/'
    for j in os.listdir(path):
        print(j)
    # new = pd.DataFrame({"date": "date", "key": "key", "flag": "1", "temp": "yes"},index=[0])
    # df = df.append(new.iloc[:],ignore_index=True)

    # i = 0
    # while i<10:
    #     print(i)
    #     i+=2








