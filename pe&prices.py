#-*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import time
import math
import talib
from scipy.stats import norm
import tushare as ts
import itertools
import datetime
from datetime import datetime
from pandas import *
from pyecharts import Grid, Bar, Line, Kline, Overlap, Page

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print("running under："+dir_path)

# draw picture
class test():
    
    def __init__(self,data_price,data_pe):
        self.data_price = data_price['close'].sort_index()
        self.data_pe = data_pe
        #print(self.data_pe.head(3))
        #print(self.data_price.head(3))
        self.price_timeline = pd.to_datetime(self.data_price.index)
        self.pe_timeline = pd.to_datetime(self.data_pe.index)
        #print(self.pe_timeline)
        #print(self.price_timeline)
        self.draw()
        
    def draw(self):
        
        line_price = Line()
        line_price.add('Close', self.price_timeline, self.data_price, is_datazoom_show=True, datazoom_type='both', datazoom_xaxis_index=[0, 1], is_fill=False, line_opacity=0.8, is_smooth=True)
        line_pe = Line()
        line_pe.add('EPS', self.pe_timeline, self.data_pe, is_fill=False, line_opacity=0.8, is_smooth=True, legend_top='58%')

        grid = Grid(width=1000, height=700)
        grid.add(line_price, grid_bottom="50%")
        grid.add(line_pe, grid_top="60%")
        
        page = Page()
        page.add(grid)
        page.render()

# set global parameter
stock_No = '000725.SZ'
end = datetime(year=2017,month=12,day=31) #开始时间结束时间
start = datetime(end.year-10,end.month,end.day)

# get data
pe_data = pd.read_excel(dir_path + '/eps_ttm.xlsx')
stock_price = pd.read_csv(dir_path + '/000725.csv')
JDA_PE = pe_data.T[stock_No][start:end]
stock_price = stock_price.set_index('time')
stock_price.index = pd.to_datetime(stock_price.index)
JDA_Price = stock_price['close'][start:end]


bt = test(stock_price,JDA_PE)

