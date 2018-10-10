import tushare as ts
import numpy as np
import pandas as pd
import os
import time

pro = ts.pro_api()
dir_path = os.path.dirname(os.path.realpath(__file__))

timelist = pd.read_csv(dir_path + '/data/trading_timelist.csv',index_col='time',parse_dates=True)
pe = pd.read_csv(dir_path + '/data/pe.csv',index_col='stock_code')
trading_timelist = list(timelist.index)
all_stock_code = list(pe.index)

def get_pe_pb():
    pe_df = pd.read_csv(dir_path + '/data/pe.csv')
    pb_df = pd.read_csv(dir_path + '/data/pb.csv')
    pe_df = pe_df.set_index('S_INFO_WINDCODE')
    pb_df = pb_df.set_index('S_INFO_WINDCODE')

    n = 0
    for i in trading_timelist[trading_timelist.index(20180831):]:
        print(i)
        n += 1
        df = pro.daily_basic(ts_code='', trade_date='%d'%i)
        df = df.set_index('ts_code')
        pe_df[i] = df['pe_ttm']
        pb_df[i] = df['pb']
        if n % 50 == 0:
            print('save to %d'%i)
            pe_df.to_csv(dir_path + '/data/pe.csv')
            pb_df.to_csv(dir_path + '/data/pb.csv')

    pe_df.to_csv(dir_path + '/data/pe.csv')
    pb_df.to_csv(dir_path + '/data/pb.csv')

def get_sz_index():
    max_collect_period = 1000
    n = len(trading_timelist)//max_collect_period
    sz_index = pd.DataFrame()
    for i in range(0,n):
        df = pro.index_daily(ts_code='000001.SH',start_date='%d'%trading_timelist[i*max_collect_period],end_date='%d'%trading_timelist[(i+1)*max_collect_period-1])
        df = df.set_index('trade_date')
        df = df.sort_index()

        if i == 0:
            sz_index = df['close']
        else:
            sz_index = pd.concat([sz_index,df['close']])

    df_more = pro.index_daily(ts_code='000001.SH',start_date='%d'%trading_timelist[n*max_collect_period],end_date='%d'%trading_timelist[-1]) 
    df_more = df_more.set_index('trade_date')
    df_more = df_more.sort_index()
    sz_index = pd.concat([sz_index,df_more['close']])
    sz_index.to_csv(dir_path + '/data/sz_index.csv')

def get_financial_ratios(ratios_name):
    final_data_df = pd.DataFrame(index=trading_timelist)
    temp_data_df = pd.DataFrame()
    for i in all_stock_code:
        print(i)
        df = pro.fina_indicator(ts_code=i,start_date='20010101')
        df = df.set_index('end_date')
        target_df = df[ratios_name]
        target_df = target_df[~target_df.index.duplicated(keep='first')]
        target_df.index = pd.to_datetime(target_df.index)
        if temp_data_df.empty:
            temp_data_df = target_df
        else:
            temp_data_df = pd.concat([temp_data_df,target_df], axis=1)
    temp_data_df.columns = all_stock_code
    temp_data_df.index = timelist_match(temp_data_df.index)
    final_data_df = pd.concat([final_data_df,temp_data_df], axis=1)
    final_data_df = final_data_df.fillna(method='bfill',limit=60)
    final_data_df = final_data_df.T
    
    final_data_df.to_csv(dir_path + '/data/%s.csv'%ratios_name)


def timelist_match(new_data_index):   
    new_data_index = list(new_data_index)
    for i in range(0,len(new_data_index)):
        for j in range(0,len(timelist.index)):
            if new_data_index[i].year == timelist.index[j].year:
                if new_data_index[i].month == timelist.index[j].month:                   
                    if new_data_index[i].day == timelist.index[j].day:
                        break
                    if timelist.index[j+1].month != timelist.index[j].month:
                        new_data_index[i] = new_data_index[i].replace(day=timelist.index[j].day)
    return new_data_index


#get_financial_ratios('debt_to_eqt')
#get_financial_ratios('current_ratio')
get_financial_ratios('basic_eps_yoy')

