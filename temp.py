import utils.point
import utils.deal
import utils.line

import os
if __name__ == '__main__':
    listFeq = ['30']
    for i in listFeq:
        # path = 'D:/project/data/stock/normal/' + i + '/'
        # target_path = 'D:/project/data/stock/simple/' + i + '/'
        # for j in os.listdir(path):
        #     utils.point.simpleTrend(path + j, target_path + j)

        #
        # path = 'D:\project\data\stock\\deal\\' + i + '\\'
        # target_path = 'D:\project\data\stock\\line\\' + i + '\\'
        # for file_code in os.listdir(path):
        #     utils.line.find_line(path + file_code, target_path + file_code)


        path = 'D:\project\data\stock\simple\\' + i + '\\'
        target_path = 'D:\project\data\stock\\deal\\' + i + '\\'
        for file_code in os.listdir(path):
            utils.deal.find_point(path + file_code, target_path + file_code)

