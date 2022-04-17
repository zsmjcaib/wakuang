import utils.point
import utils.deal
import utils.line
from multiprocessing import Process
import pandas as pd
import os





def process(i,s,e):




    path = 'D:/project/data/stock/normal/' + i + '/'
    target_path = 'D:/project/data/stock/simple/' + i + '/'
    for j in os.listdir(path)[s:e]:
        if  os.path.exists(target_path + j):
            continue
        df = pd.read_csv(path+j)
        df_simple = df.iloc[0:10, 0:7].copy()
        df_simple = utils.point.simpleTrend(df, df_simple)
        df_simple.to_csv(target_path + j, index=False)



    path = 'D:\project\data\stock\simple\\' + i + '\\'
    target_path = 'D:\project\data\stock\\deal\\' + i + '\\'
    for j in os.listdir(path)[s:e]:
        df = pd.read_csv(path+j)
        df_point = pd.DataFrame(columns=['date','key','flag','temp'])
        df_point = utils.deal.find_point(df, df_point)
        df_point.to_csv(target_path + j, index=False)


    path = 'D:/project/data/stock/deal/'+ i + '/'
    target_path = 'D:/project/data/stock/line/'+ i + '/'
    for j in os.listdir(path)[s:e]:
        df = pd.read_csv(path + j)
        df_line = pd.DataFrame(columns=['date', 'key', 'flag', 'temp','small_to_large','first','second'])
        df_line = utils.line.find_line(df, df_line)
        df_line.to_csv(target_path + j, index=False)

if __name__ == '__main__':
    path = 'D:/project/data/stock/normal/' + '5' + '/'
    total = len(os.listdir(path))
    each = int(total / 4)
    p1 = Process(target=process,args=('5',0,each,))

    p2 = Process(target=process,args=('30',0,total,))
    p3 = Process(target=process,args=('5',each,2*each,))
    p4 = Process(target=process,args=('5',2*each,3*each,))
    p5 = Process(target=process,args=('5',3*each,4*each,))
    p6 = Process(target=process,args=('5',4*each,total+1,))
    # p3 = Process(target=process,args=('day',))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    # process('30',0,each)

