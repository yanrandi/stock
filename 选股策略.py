# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 10:30:45 2021
RPS选股策略
@author: yanra
"""
import efinance as ef
import time
from datetime import datetime
import datetime
import pandas as pd
import numpy as np
from sklearn import preprocessing

        
#获取近20日所有日k的数据
data = ef.stock.get_realtime_quotes()
code_list = list(data['股票代码'])
d1 = datetime.date.today()
d2 = d1 + datetime.timedelta(-30)
d1_str = str(d1).replace('-','')
d2_str = str(d2).replace('-','')
stock_data_20 = ef.stock.get_quote_history(code_list,beg = d2_str,end = d1_str)
#计算近20日的涨跌幅
sample_value_list = []
for item in stock_data_20.keys():
    # sample_key_list.append(item)                    '''收集字典的键'''
    sample_value_list.append(stock_data_20[item])

#将list结构转为dataframe
rsi_stock_data = pd.concat(sample_value_list)
#分组求和，计算涨跌幅
rsi_stock_data['涨跌幅'] = rsi_stock_data['涨跌幅'].astype(float)
t_data = pd.pivot_table(rsi_stock_data,values = '涨跌幅',index = ['股票代码','股票名称'],aggfunc=sum).reset_index()
t_data1=t_data[~t_data['股票名称'].str.contains('ST')]
t_data1=t_data1[~t_data1['股票名称'].str.contains('N')]
t_data1=t_data1[~t_data1['股票名称'].str.contains('C')]
t_data1=t_data1[t_data1['涨跌幅']<=110]
#对涨跌幅进行排序,并且计算分值映射到0-1000
t_data2 = t_data1.sort_values(by="涨跌幅",ascending=False)
# def minmax_norm(df_input):
#     return (df_input - df_input.min()) / ( df_input.max() - df_input.min())
# minmax_norm_data = minmax_norm(t_data2['涨跌幅'])*100
t_data2['百分位'] = t_data2['涨跌幅'].rank(pct=True)
t_data2 = t_data2[t_data2['百分位']>=0.87]
#计算当日的成交额,筛选成交额大于2亿的股票
data_date = rsi_stock_data[rsi_stock_data['日期']== str(d1)]

data_date = data_date[data_date['成交额']>=200000000]
#拼接
new_data = pd.merge(t_data2,data_date[['股票代码','成交额']],how='left',on = '股票代码')
#筛选 
new_data = new_data[~new_data['成交额'].isnull()]
new_data['成交额'] = new_data['成交额']/100000000
code_list = list(new_data['股票代码'])
stock_base = ef.stock.get_base_info(code_list)
stock_base = stock_base[['股票代码','所处行业']]
#
rsi_last_data = pd.merge(new_data,stock_base,how='left',on = '股票代码')

rsi_last_data = rsi_last_data.sort_values(by="成交额",ascending=False)


