import tushare as ts
import pandas as pd
import numpy as np
import os
import statsmodels.api as sm

dir_path = os.path.dirname(os.path.realpath(__file__))
print("running under："+ dir_path)


DJ = pd.read_csv(dir_path + '/道琼斯指数.csv')
hs300 = ts.get_hist_data('hs300')
shzh = ts.get_hist_data('sh')

hs300 = hs300['close']
shzh = shzh['close']

hs300 = hs300.sort_index()
hs300.index = pd.to_datetime(hs300.index)
shzh = shzh.sort_index()
shzh.index = pd.to_datetime(shzh.index)
DJ['Date'] = pd.to_datetime(DJ['Date'], format = '%d/%m/%Y')
DJ = DJ.set_index('Date')

DJ_return = DJ.diff()/DJ
hs300_return = hs300.diff()/hs300
shzh_return = shzh.diff()/shzh

all_data = pd.concat([DJ_return, hs300_return, shzh_return], axis=1, join='inner')
all_data = all_data.dropna()
all_data.columns = ['DJ','HS300','SZ']

x_array = all_data['DJ'].as_matrix(columns=None)
y_array = all_data['SZ'].as_matrix(columns=None)
x_array = sm.add_constant(x_array)
result = sm.OLS(y_array, x_array).fit()


