
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
      
    









