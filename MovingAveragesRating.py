#!/usr/bin/env python
# coding: utf-8

# In[20]:


# call 
import numpy as np
import pandas as pd
import sys
import datetime


# In[21]:


def rating(ma_short, ma_median, ma_long):
    # Rate the stocks by 3 MAs.
    if ma_short >= ma_median and ma_median >= ma_long:
        rating = 1
    elif ma_median > ma_short and ma_short >= ma_long:
        rating = 2
    elif ma_median >= ma_long and ma_long > ma_short:
        rating = 3
    elif ma_long > ma_median and ma_median > ma_short:
        rating = 4
    elif ma_long > ma_short and ma_short >= ma_median:
        rating = 5
    #elif ma_short >= ma_long and ma_long > ma_median:
    #    rating = 6
    else: 
        rating = 6
        
    return rating


# In[22]:


# def getIncrementalRatings(frequency, d):
#     section = 0
#     if frequency == 'w':
#         # can fix later to have it be exact week
#         section = 7
#     elif frequency == 'm':
#         # can fix later to have it be exact months
#         section = 30
#     else:
#         section = 365
    
#     assets = []
    
#     # get ratings in incremental orders
#     #print(len(d[0]))
#     #print(d[0])
# #    return
# #    for company in d:
        
#     assets.append(d.iloc[range(0, len(d), section)])
        
#     #print(assets)
#     return assets


# In[23]:


def date2Days(date):
    # format is string xx-xx-xxxx
    #print(date)
    comp = date.split('-')
    day = 0
    day += (int(comp[2]) * 365)
    day += (int(comp[1]) * 30)
    day += (int(comp[0]))
    # should really be subtracting 1 from the month, but it really doesn't matter
    #print(day)
    return day


# In[24]:


def getFrequencyRange(data, frequency, start_idx, end_idx):
    sub_indices = [start_idx]
    freq = 1
    if frequency == 'w':
        # can fix later to have it be exact week
        freq = 7
    elif frequency == 'm':
        # can fix later to have it be exact months
        freq = 30
    elif frequency == 'y':
        freq = 365
    # get the subset of data based on days, weeks, months, or years
    
    cur_day = date2Days(data.iloc[start_idx]['date'])
    
    for i in range(start_idx+1, end_idx+1):
        if date2Days(data.iloc[i]['date']) >= (cur_day+freq):
            sub_indices.append(i)
            cur_day = date2Days(data.iloc[i]['date'])
    #print(sub_indices)
    return sub_indices

# need to pass in start and end data frequency (d= days, w=weeks, m=months, y=years) and list of companies
def get_MA_Ratings(MA):

    # round to whole number
    MA['Price'] = np.round(MA['close'])

    MA['20d'] = np.round(MA['close'].rolling(window =20, center = False).mean(),2)

    MA['50d'] = np.round(MA['close'].rolling(window =50, center = False).mean(),2)

    MA['200d'] = np.round(MA['close'].rolling(window =200, center = False).mean(),2)

    MA['SMA_rating'] = MA.apply(lambda x: rating(x['Price'], x['50d'], x['200d']), axis=1)
    MA['SMA_rating'] = MA.apply(lambda x: rating(x['Price'], x['50d'], x['200d']), axis=1)
    MA['SMA_rating'] = MA.apply(lambda x: rating(x['Price'], x['50d'], x['200d']), axis=1)
    MA = pd.DataFrame(MA, columns=['date','SMA_rating'])
    return MA

