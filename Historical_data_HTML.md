# Trend strength
Trend strength indicator based on moving average
```py
# import library
import pandas as pd
import numpy as np
import math
import warnings
warnings.filterwarnings("ignore")
from copy import deepcopy
from pandas import Series,DataFrame

import matplotlib.pyplot as plt
plt.rcParams['font.serif'] = ['KaiTi']     #用来正常显示中文
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
import seaborn as sns
sns.set_style({"font.sans-serif":['KaiTi', 'Arial']},{"axes.unicode_minus":False})

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print("running under："+dir_path)
def clear():os.system('cls')

import datetime
import time
start_time = time.time()
############################################################################

# import data
data = pd.read_csv(dir_path+'/000725.csv')

# get daily return
data['daily_return'] = 0.00
for i in range(0,len(data)-1):
    data['daily_return'][i+1] = data['Close'][i+1]/data['Close'][i]-1

# 5-day & 10-day volatility
data['5-day vol'] = pd.rolling_std(data['daily_return'][1:], window=5)
data['10-day vol'] = pd.rolling_std(data['daily_return'][1:], window=10)
#####alternatives
#data['5-day vol'] = 0.00
#for i in range(1,len(data)-4): 
#    data['5-day vol'][i+4] = np.std(data['daily_return'][i:i+5],ddof=1)

############################################################################

def trend_strength(data,day_number,columns_name):
    
    for i in range(1,len(data)-day_number+1):
        actual_return_series = data.iloc[i:i+day_number,6]
        actual_return_list = list(actual_return_series)
        exp_return_series = abs(actual_return_series).sort_values()
        exp_return_list = list(exp_return_series)
        actual_netvalue = []
        exp_netvalue = []
        pre_value = 1
        exp_pre_value = 1
        
        for x in range(0,day_number):
            actual_netvalue.append(pre_value*(actual_return_list[x]+1))
            pre_value *= (actual_return_list[x]+1) # actual net value series
        for x in range(0,day_number):
            exp_netvalue.append(exp_pre_value*(exp_return_list[x]+1))
            exp_pre_value *= (exp_return_list[x]+1) # hypothetic net value series
        
        actual_bias = (actual_netvalue[day_number-1] - np.mean(actual_netvalue))/np.mean(actual_netvalue)
        exp_bias = (exp_netvalue[day_number-1] - np.mean(exp_netvalue))/np.mean(exp_netvalue)
        data[columns_name][i+day_number-1] = actual_bias/exp_bias


# 1-5 MA
data['1-5 MA'] = 0.00
columns_name = '1-5 MA'
trend_strength(data,5,columns_name)

#1-10 MA
data['1-10 MA'] = 0.00
columns_name = '1-10 MA'
trend_strength(data,10,columns_name)

############################################################################

def volaility_percentile(data,start_day,end_day,base_column_name,new_column_name):
    data[new_column_name] = 0.00
    maxi = max(data[base_column_name][start_day:end_day])
    mini = min(data[base_column_name][start_day:end_day])
    for i in range(end_day+1,len(data)):
        vol_percentile = (data[base_column_name][i]-mini)/(maxi-mini)
        data[new_column_name][i] = vol_percentile

# 5-day vol percentile
base_column_name = '5-day vol'
new_column_name = '5_vol'
volaility_percentile(data,5,100,base_column_name,new_column_name)

# 10-day vol percentile
base_column_name = '10-day vol'
new_column_name = '10_vol'
volaility_percentile(data,10,100,base_column_name,new_column_name)

data = data.set_index('Time')
data = data.reindex(columns=['Open','Close','High','Low','Volume','1-5 MA','1-10 MA','5_vol','10_vol'])
trendindex_data = data.iloc[102:,:]
trendindex_data.to_csv(dir_path+'trend.csv')
```
# Scalable HTML chart with 3-dimensions of historical data

```py
#-*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import time
import math
import talib
from scipy.stats import norm
import tushare as ts
import itertools 
from datetime import datetime
from pyecharts import Grid, Bar, Line, Kline, Overlap, Page


class CTA():
    def __init__(self, Quote_frame):

        self.data = Quote_frame #取该股票的所有数据
        self.data = self.data.sort_index()
        self.price = self.data[['open', 'close', 'high', 'low']] #取要画k线的4列数据 
        self.price_list = [self.price.ix[i].tolist() for i in range(len(self.price))]
        self.timeline = pd.to_datetime(self.data.index) #定义时间轴
        #self.volume = self.data['volume'] #取data中的成交量数据

        # 依次运行所有内置函数
        self.basic_cal()
        self.allin()
        
        self.draw()

    def basic_cal(self):
        # get daily return
        self.ret = self.data['price_change']/self.data['close']       

        # 5-day & 10-day volatility
        self.std_5 = pd.rolling_std(self.ret, window=5)
        self.std_10 = pd.rolling_std(self.ret, window=10)



    def trend_strength(self,day_number,columns_name):
    
        for i in range(1,len(self.data)-day_number+1):
            actual_return_series = self.ret.iloc[i:i+day_number]
            actual_return_list = list(actual_return_series)
            exp_return_series = abs(actual_return_series).sort_values()
            exp_return_list = list(exp_return_series)
            actual_netvalue = []
            exp_netvalue = []
            pre_value = 1
            exp_pre_value = 1
            
            for x in range(0,day_number):
                actual_netvalue.append(pre_value*(actual_return_list[x]+1))
                pre_value *= (actual_return_list[x]+1) # actual net value series
            for x in range(0,day_number):
                exp_netvalue.append(exp_pre_value*(exp_return_list[x]+1))
                exp_pre_value *= (exp_return_list[x]+1) # hypothetic net value series
            
            actual_bias = (actual_netvalue[day_number-1] - np.mean(actual_netvalue))/np.mean(actual_netvalue)
            exp_bias = (exp_netvalue[day_number-1] - np.mean(exp_netvalue))/np.mean(exp_netvalue)
            self.data[columns_name][i+day_number-1] = actual_bias/exp_bias


    def volaility_percentile(self,data,start_day,end_day,new_column_name):
        
        self.data[new_column_name] = 0.00
        maxi = max(data[start_day:end_day])
        mini = min(data[start_day:end_day])
        for i in range(end_day+1,len(data)):
            vol_percentile = (data[i]-mini)/(maxi-mini)
            self.data[new_column_name][i] = vol_percentile

        

    def draw(self):#在初始化函数被调用

        kline = Kline('Stock Prices')
        kline.add('Candle Line', self.timeline, self.price_list, is_datazoom_show=True, datazoom_type='both', datazoom_xaxis_index=[0, 1, 2]) #画k线图

        line = Line()
        line.add('close', self.timeline, self.data['close'], is_fill=False, line_opacity=0.8, is_smooth=True)
        line.add('MA_5', self.timeline, self.data['ma5'], is_fill=False, line_opacity=0.8, is_smooth=True)
        line.add('MA_10', self.timeline, self.data['ma10'], is_fill=False, line_opacity=0.8, is_smooth=True)
        line.add('MA_20', self.timeline, self.data['ma20'], is_fill=False, line_opacity=0.8, is_smooth=True)

        overlap = Overlap() #画在同一个图上
        overlap.add(kline)
        overlap.add(line)

        line_trend = Line("Trending Index", title_top="60%")
        line_trend.add('1-5MA', self.timeline, self.data['1-5 MA'], is_fill=False, line_opacity=0.8, is_smooth=True,  legend_top="55%")
        line_trend.add('1-10MA', self.timeline, self.data['1-10 MA'], is_fill=False, line_opacity=0.8, is_smooth=True,  legend_top="55%")

        line_std = Line("Volatility Index", title_top="80%")
        line_std.add('5vol', self.timeline, self.data['5_vol'], is_fill=False, line_opacity=0.8, is_smooth=True, legend_top="80%")
        line_std.add('10vol', self.timeline, self.data['10_vol'], is_fill=False, line_opacity=0.8, is_smooth=True, legend_top="80%")


        grid = Grid(width=1400, height=1100)
        grid.add(overlap, grid_bottom="50%")
        grid.add(line_trend, grid_top="55%",grid_bottom="25%")
        grid.add(line_std, grid_top="85%")

        page = Page()
        page.add(grid)
        page.render()


    def allin(self):
        # 1-5 MA
        self.data['1-5 MA'] = 0.00
        columns_name = '1-5 MA'
        self.trend_strength(5,columns_name)

        #1-10 MA
        self.data['1-10 MA'] = 0.00
        columns_name = '1-10 MA'
        self.trend_strength(10,columns_name)
        
        # 5-day vol percentile
        new_column_name = '5_vol'
        self.volaility_percentile(self.std_5,5,100,new_column_name)

        # 10-day vol percentile
        new_column_name = '10_vol'
        self.volaility_percentile(self.std_10,10,100,new_column_name)

    


if __name__ == '__main__':
    end = datetime.today() #开始时间结束时间，选取最近一年的数据
    start = datetime(end.year-2,end.month,end.day)
    end = str(end)
    start = str(start)
    stock_No = '000725'
    
    Quote_frame = ts.get_hist_data(stock_No,start,end)
    bt = CTA(Quote_frame)

```

# Picture
![candle chart](https://github.com/YourongYe/Quant-project/blob/master/Stock%20Prices.png)
    









