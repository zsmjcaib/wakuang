import pandas as pd
import yaml
from multiprocessing import Process
from datetime import date,timedelta
import datetime
import time
from multiprocessing import Lock
import multiprocessing as mp
from update import update
from utils.strategy_buy import strategy
from utils.util import read_record
from dingtalkchatbot.chatbot import DingtalkChatbot
from utils.regression_tool import init

def start(target_codes,content,lock):
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=2756f159af5640625e07d7733734afa59a4d1926d70871b5e8ad0d3eab217e88'
    robot = DingtalkChatbot(webhook)

    beg = 'all'
    now = datetime.datetime.now()
    date = now.date().strftime('%Y-%m-%d')
    open_time = datetime.datetime.strptime(date + ' ' + '09:30:00', "%Y-%m-%d %H:%M:%S")
    close_time = datetime.datetime.strptime(date + ' ' + '15:05:00', "%Y-%m-%d %H:%M:%S")
    close_noon = datetime.datetime.strptime(date + ' ' + '11:35:00', "%Y-%m-%d %H:%M:%S")
    open_noon = datetime.datetime.strptime(date + ' ' + '13:00:00', "%Y-%m-%d %H:%M:%S")
    time_point = [open_time, close_noon, open_noon, close_time]
    while time_point:
        mark_start = time.time()
        if time_point[0] < now:
            time_point.pop(0)
            continue
        diff = (time_point[0] - now).seconds
        if len(time_point) % 2 == 0:
            sleep = diff - 30
            time.sleep(sleep if sleep > 0 else 11)
            continue
        else:
            codes = target_codes['code'].tolist()
            update(codes,content,beg)
            beg = 'today'
            for code in codes:
                result = strategy(content,code+'.csv')
                if result !='':
                    robot.send_text('我比sbf少个f'+' '+result)


        mark_end = time.time()
        print('睡眠')
        time.sleep(300 - mark_end + mark_start)


if __name__ == '__main__':
    with open('config.yaml') as f:
        content = yaml.load(f,Loader=yaml.FullLoader)
        f.close()
    target_codes = pd.read_csv(content['list_path']+'list.csv',converters={'code': str})
    for index,code in target_codes.iterrows():
        if code['init'] ==0:
            init(code['code']+'.csv',content)
            target_codes['init'].iloc[index] = 1
            target_codes.to_csv(content['list_path']+'list.csv',index=False)
    lock = mp.Lock()
    #
    # p1 = Process(target=start, args=(target_codes,content,lock))
    # # p2 = Process(target=start, args=())
    #
    # p1.start()
    # start(target_codes,content,lock)







