import pandas as pd
import os
if __name__ == '__main__':
 data = pd.DataFrame({'a':[0,10,20,30,40],'b':[1,11,21,31,41],'c':[2,12,22,32,42]})
 print(data)
 print(data.iloc[3]["a"])
 print(data.loc[3]["a"])








