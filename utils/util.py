import pandas as pd
import os
def read_record(path,code,flag):
    if not os.path.exists(path + code+'_'+flag):
        demo = pd.DataFrame(columns=['date','buy_price','sell_price','high_price','net'])
        demo.loc[len(demo)] = [ "", "","", "","1"]
    else:
        demo = pd.read_csv(path + code+'_'+flag)
    return demo