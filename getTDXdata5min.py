import os
import struct
import math
import utils.getMacd as getMacd
import pandas as pd

# 根据二进制前两段拿到日期分时
def get_date_str(h1, h2) -> str:  # H1->0,1字节; H2->2,3字节;
    year = math.floor(h1 / 2048) + 2004  # 解析出年
    month = math.floor(h1 % 2048 / 100)  # 月
    day = h1 % 2048 % 100  # 日
    hour = math.floor(h2 / 60)  # 小时
    minute = h2 % 60  # 分钟
    if hour < 10:  # 如果小时小于两位, 补0
        hour = "0" + str(hour)
    if minute < 10:  # 如果分钟小于两位, 补0
        minute = "0" + str(minute)
    return str(year) +'-' + str(month) +'-' + str(day)+' '  + str(hour) +':' + str(minute)


# 根据通达信.lc5文件，生成对应名称的csv文件
def stock_lc5(file, target_file) -> None:
    # (通达信.lc5文件路径, 通达信.lc5文件名称, 处理后要保存到的文件夹)
    with open(file, 'rb') as f:  # 读取通达信.lc5文件，并处理
        file_object = open(target_file, 'w+')  # 打开新建的csv文件，开始写入数据
        title_list = "date,open,high,low,close,amount,vol,diff,dea,macd\n"  # 定义csv文件标题
        file_object.writelines(title_list)  # 将文件标题写入到csv中

        while True:
            li2 = f.read(32)  # 读取一个5分钟数据
            if not li2:  # 如果没有数据了，就退出
                break
            data2 = struct.unpack('HHffffllf', li2)  # 解析数据
            date_str = get_date_str(data2[0], data2[1])  # 解析日期和分时

            data2_list = list(data2)  # 将数据转成list
            data2_list[1] = date_str  # 将list二个元素更改为日期 时:分
            del (data2_list[0])  # 删除list第一个元素
            del (data2_list[-1])

            list3 = data2_list[0] + "," + \
                   str(round(data2_list[1],2)) + "," + str(round(data2_list[2],2)) + "," + str(
                round(data2_list[3],2)) + "," + str(round(data2_list[4],2)) + "," + str(data2_list[5]) + "," + str(
                data2_list[6]) + "\n"
            file_object.writelines(list3)

        file_object.close()  # 完成数据写入
        df = pd.read_csv(target_file)
        data = getMacd.stock_macd(df)
        data.tocsv(target_file, index=0)


"""
# 设置通达信.day文件所在的文件夹
path_dir = 'D:/app/new_jyplug/vipdoc/'+l+'/lday/'+'fzline\\'
# 设置数据处理好后，要将csv文件保存的文件夹
target_dir = '../lc5/'
# 读取文件夹下的通达信.day文件
listfile = os.listdir(path_dir)
# 逐个处理文件夹下的通达信.day文件，并生成对应的csv文件，保存到../day/文件夹下
for fname in listfile:
    stock_lc5(path_dir + fname, fname, target_dir)
else:
    print('The for ' + path_dir + ' to ' + target_dir + '  loop is over')
    print("文件转换已完成")
"""
if __name__ == '__main__':
    list1=["sh","sz"]
    file_object_path = 'D:/project/data/stock/normal/5/'

    for l in list1:
        path = 'D:/app/new_jyplug/vipdoc/' + l + '/fzline/'
        listfile = os.listdir(path)
        for i in listfile:
            if i.startswith("0",2)|i.startswith("30",2)|i.startswith("60",2):
                stock_lc5(path + i, file_object_path+i[2:-4]+'.csv')
