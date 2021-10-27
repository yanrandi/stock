# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 17:04:51 2021
大额成交追涨策略
@author: yanra
"""
import efinance as ef
import time
from datetime import datetime
import datetime
import pandas as pd
import numpy as np
import schedule
from datetime import datetime
import time
def job(*args):
    data = ef.stock.get_realtime_quotes()
    code_list = list(data['股票代码'])
    
    data = data[data['成交额']!='-']
    data['成交额'] =data['成交额'].astype(float) 
    #选取前20的成交最大的股票
    data = data.sort_values(by ='成交额',ascending = False)
    data['成交额'] = data['成交额']/100000000
    data = data.iloc[:30,:]
    data['流通市值'] = data['流通市值'].astype(float)
    data['市值判断'] = np.where((data['流通市值']/100000000)>=500,1,0)
    data1 = data[['股票名称','涨跌幅','成交额','市值判断']]
    print(data1)
    
schedule.every(30).seconds.do(job)

if __name__ == '__main__':
    while True:
        # 启动服务
        schedule.run_pending()


