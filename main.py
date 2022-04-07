import utils.point
import utils.deal
from multiprocessing import Process

import os





def process(freq):


    # listFeq = ['5','30']
    # for i in listFeq:
    #     path = 'D:/project/data/stock/normal/' + i + '/'
    #     target_path = 'D:/project/data/stock/simple/' + i + '/'
    #     for j in os.listdir(path)[0:int((len(os.listdir(path))+1)/2)]:
    #         utils.point.simpleTrend(path + j, target_path + j)

    target = freq
    for i in target:
        path = 'D:\project\data\stock\simple\\' + i + '\\'
        target_path = 'D:\project\data\stock\\deal\\' + i + '\\'
        for file_code in os.listdir(path)[int((len(os.listdir(path))+1)/2):len(os.listdir(path))]:
            utils.deal.find_point(path + file_code, target_path + file_code)
    """
    listFeq = ['30', '5']
    for i in listFeq:
        path_dir = 'D:/project/data/stock/simple/'+ i + '/'
        target_path_dir = 'D:/project/data/stock/analysis/'+ i + '/'
        utils.point.find_point(path_dir,target_path_dir)
"""
if __name__ == '__main__':
    p1 = Process(target=process,args=('5',))
    p2 = Process(target=process,args=('30',))
    p3 = Process(target=process,args=('day',))

    p1.start()
    p2.start()
    p3.start()


