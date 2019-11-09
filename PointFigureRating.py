#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd
import sys
import math


# In[37]:


# (price range, box size)
box_ranges = [(.25,.0625),
              (1,.125), 
              (5,.25),
              (20,.5),
              (100,1),
              (200,2),
              (500,4),
              (1000,5),
              (25000,50),
              (sys.maxsize,500)]


# In[38]:


def updateBoxSize(price):
    
    for i in range (len(box_ranges)):
        if price < box_ranges[i][0]:
            return box_ranges[i][1]
    return None

#     if XO == 'X':
#         for i in range(len(box_ranges)):
#             if high < box_ranges[i][1]:
#                 return box_sizes[i]
#     else:
#         for i in range(len(box_ranges)):
#             if low < box_ranges[i][1]:
#                 return box_sizes[i]
            
#     # should never get to here but just to be safe
#     return None# returns 2


# In[52]:


# going to assume the scale starts at 0
# this is going to return the value of the box that is rounded down to the nearest box_size
def updateBoxPrice(price, box_size, XO):
    if XO == 'X':
        if box_size >= 1:
            return price - (price % box_size)
        else:
            inter = math.ceil(price)
            while inter > price:
                inter = inter - box_size
            return inter
    else:
        if box_size >= 1:
            return price - (price % box_size) + box_size
        else:
            inter = int(price)
            while inter < price:
                inter = inter + box_size
            return inter
# def updateBoxPriceO(high, low, XO, box_size, adj_close):

#     return adj_close - (adj_close % box_size)+box_size
        
        
#     if XO == 'X':
#         mod_val = high % box_size
#         return high - mod_val
#     else:
#         mod_val = low % box_size
#         return low - mod_val


# In[53]:


def add_boxes(old_price, new_price, box_size, XO):
    
    boxes_diff = updateBoxPrice(old_price, box_size, XO) - updateBoxPrice(new_price, box_size, XO)
    #print(str(inter/box_size))
    return abs(int(boxes_diff/box_size))
    


# In[118]:


def column_X (reversal, df, row):
    # try adding an X with the high price.
    # if can't add an X:
    # try low and if it creates a 3 box reversal, then use that
    # otherwise do nothing
    box_size = updateBoxSize(row['high'])
    box_price = updateBoxPrice(row['high'], box_size, 'X')
    
  #  added_boxes = add_boxes(row['high'], df[-1]['high'], box_size, 'X')
  #  sub_boxes = add_boxes(df[-1]['low'], row['low'], box_size, 'X')    
#     print("X added_boxes: " + str(added_boxes))
#     print("X sub_boxes: " + str(sub_boxes))    
#     print('X box_high: ' + (str(df[-1]['box_high'])))
#     print('X box_low: ' + (str(df[-1]['box_low'])))    
#     print('X high: ' + str(df[-1]['high']))    
#     print('X low: ' + str(df[-1]['low']))
#     print('X date: ' +row['date'])        
    
    if row['high'] >= df[-1]['box_high']+box_size:
       # print(row['high'])
        df[-1]['box_high'] = updateBoxPrice(row['high'],box_size,'X')
        
        df[-1]['high'] = row['high']               
        
#         if row['low'] < df[-1]['low']: 
#             df[-1]['low'] = row['low']       
        
        df[-1]['date_end'] = row['date']
        df[-1]['day'][row['date']] = {'box_high': df[-1]['box_high'], 
                                    'box_low' : df[-1]['box_low'],
                                      'high':row['high'],
                                      'low':row['low'],
                                      'close':row['close'],
                                         'box_size':box_size}
        
    elif row['low'] <= df[-1]['box_high']-((reversal)*box_size):
         
        # creating a new column of Os        
        df_temp = {'date_start':row['date'],
                    'date_end':row['date'],
                    'XO':'O', # the high and low shouldn't matter because we are comparing box prices
                    'high': row['high'],
                    'low': row['low'],
                    'box_high': (df[-1]['box_high']-box_size),# here we need to append the boxes to the O column to start at the box right below the highest box in the X column
                    'box_low': updateBoxPrice(row['low'],updateBoxSize(row['low']),'O'),
                    'day':{row['date']:
                        {'box_high':(df[-1]['box_high']-box_size), 
                        ""'box_low' : updateBoxPrice(row['low'],updateBoxSize(row['low']),'O'),
                        'high':row['high'],
                         'low':row['low'],
                         'close':row['close'],
                        'box_size':box_size}}}
        df.append(df_temp)
    else:
        # if no movement in column
        df[-1]['date_end'] = row['date']
        df[-1]['day'][row['date']] = {'box_high': df[-1]['box_high'],
                                      'box_low' : df[-1]['box_low'],
                                      'high':row['high'],
                                      'low':row['low'],
                                      'close':row['close'],
                                     'box_size' : box_size}
        
    return df


# In[147]:


def column_O (reversal, df, row):
    # use the low if you can create a new O box
    # use the high when another O can't be drawn and we creates a 3 box reversal
    # ignore else
    
    box_size = updateBoxSize(row['close'])
    box_price = updateBoxPrice(row['close'], box_size, 'O')
 
    sub_boxes = add_boxes(row['low'],df[-1]['low'], box_size, 'O')
    added_boxes = add_boxes(row['high'],df[-1]['high'], box_size, 'O')    
#    print(added_boxes)
#    print(sub_boxes)  
#     print("O added_boxes: " + str(added_boxes))
#     print("O sub_boxes: " + str(sub_boxes))    
#     print('O box_high: ' + (str(df[-1]['box_high'])))
#     print('O box_low: ' + (str(df[-1]['box_low'])))
#     print('O high: ' + str(df[-1]['high']))    
#     print('O low: ' + str(df[-1]['low']))    
#     print('O date: ' +row['date']) 
    
    if row['low'] <= df[-1]['box_low']-box_size:


        df[-1]['box_low'] = updateBoxPrice(row['low'],box_size,'O')

        df[-1]['low'] = row['low']
        
#         if row['high'] > df[-1]['high']: 
#             df[-1]['high'] = row['high']
        
        df[-1]['date_end'] = row['date']
        
        df[-1]['day'][row['date']] = {'box_high': df[-1]['box_high'],
                                       'box_low' : df[-1]['box_low'],
                                      'high':row['high'],
                                      'low':row['low'],
                                      'close':row['close'],
                                         'box_size':box_size}
        
    elif row['high'] >= df[-1]['box_low']+((reversal)*box_size):


        df_temp = {'date_start':row['date'],
                    'date_end':row['date'],
                    'XO':'X', # the high and low shouldn't matter because we are comparing box prices
                    'high': row['high'],
                    'low': row['low'],
                    'box_high': updateBoxPrice(row['high'],updateBoxSize(row['high']), 'X'), # here we need to append the boxes to the O column to start at the box right below the highest box in the X column
                    'box_low': df[-1]['box_low'] + box_size,
                    'day':{row['date']:
                        {'box_high':updateBoxPrice(row['high'],updateBoxSize(row['high']), 'X'),
                         'box_low' : df[-1]['box_low'] + box_size,
                        'high':row['high'],
                         'low':row['low'],
                         'close':row['close'],
                            'box_size':box_size}}}
        df.append(df_temp)
    else:
        # if no movement in column
        df[-1]['date_end'] = row['date']
        df[-1]['day'][row['date']] = {'box_high': df[-1]['box_high'],
                                      'box_low' : df[-1]['box_low'],
                                      'high':row['high'],
                                      'low':row['low'],
                                      'close':row['close'],
                                         'box_size':box_size}
    return df
        


# In[148]:



def constructPFChart(data):
    # starting out, we assume that the first box is an X

    box_size = updateBoxSize(data['high'].iloc[0])
    box_price = updateBoxPrice(data['high'].iloc[0], box_size, 'X')
    
    reversal = 3
    df = []
    df_temp = {'date_start':data['date'].iloc[0], 
           'date_end':data['date'].iloc[0],
           'XO':'X',
           'high':data['high'].iloc[0],
           'low':data['low'].iloc[0],
            'box_high':box_price,
            'box_low':box_price-((reversal-1)*box_size),
            'day': {data['date'].iloc[0]:{'box_high': box_price, 
                                     'box_low' : box_price-((reversal-1)*box_size),
                                     'high':data['high'].iloc[0], 
                                     'low':data['low'].iloc[0], 
                                     'close':data['close'].iloc[0],
                                         'box_size':box_size}}}
    df.append(df_temp)

    for index, row in data.iloc[1:].iterrows():
        #print(row)
        #print()
        #print(df)
        #print()        
        # check if the previous day's column is an X or an O
        if df[-1]['XO'] == 'X':
           # print('X')
           # print(row)
            df = column_X(reversal, df, row)
        else:
           # print('O')
           # print(row)            
            df = column_O(reversal, df, row)

    return df


# In[149]:


def date2Days(date):
    # format is string xx-xx-xxxx
    #print(date)
    comp = date.split('-')
    day = 0
    day += (int(comp[2]) * 365)
    day += (int(comp[1]))
    day += (int(comp[0])*30)
    # should really be subtracting 1 from the month, but it really doesn't matter
    #print(day)
    return day


# In[150]:


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


# In[151]:


# need to replace last box price with highest and lowest box price
def get_ratings(pf_data, query_data):
    


    # need to first get start and end index
    start_column = 0
    end_column = len(pf_data)
   # print(pf_data[0])
    for i in range(len(pf_data)):
        if query_data.iloc[0]['date'] in pf_data[i]['day']:
            start_column = i
            break
            
    for i in range(start_column, len(pf_data)):
        if query_data.iloc[-1]['date'] in pf_data[i]['day']:
            end_column = i
            break
              
    # now we get the ratings
    # if X, then look at previous X's column
    # if current price is higher than previous X's column's high
    # that is a 1
    # if in a O column, and you go below the previous O column's low,
    # that is a sell mode with rating 4
    # if you're in a sell mode and you move to a column of X's, that is a rating of 3
    # if you're in a buy mode and you move into a column of O's that is a rating of 2
    # going through each date of the query data
    ratings = []
    boxes = []
    XOs = []
    for index, row in query_data.iterrows():
#        print(row['date'])
        # finding where it is in the pf chart

        while row['date'] not in pf_data[start_column]['day']:

            start_column += 1
            
#        print(pf_data[start_column]['day'][row['date']]['box_price'])
#        print(row)
        if pf_data[start_column]['XO'] == 'X':
            boxes.append(pf_data[start_column]['day'][row['date']]['box_high'])
        else:
            boxes.append(pf_data[start_column]['day'][row['date']]['box_low'])
        XOs.append(pf_data[start_column]['XO'])
        
        if pf_data[start_column]['XO'] == 'X':
            # Note: clearly 2 columns back is also an X  (gotta be careful abt -2 if we started at 0 or 1)              
            
            if boxes[-1] > pf_data[start_column - 2]['box_high']:
                ratings.append(1)
            else:
                if len(ratings) == 0:
                    ratings.append(3)
                elif ratings[-1] == 1:
                    ratings.append(1)
                else:
                    ratings.append(3)
        else:

            if boxes[-1] < pf_data[start_column - 2]['box_low']:
                ratings.append(4)
            else:
                if len(ratings) == 0:
                    ratings.append(2)
                elif ratings[-1] == 4:
                    ratings.append(4)
                else:
                    ratings.append(2)
  #  print(len(ratings))
  #  print(len(boxes))
    query_data['PF_rating'] = ratings
    query_data['box_price'] = boxes
    query_data['XO'] = XOs

    return query_data


# In[152]:


def get_PF_Ratings(full_data, asset):

    # get data
    #price = pd.read_csv(tickerFile)
    
    pf_data = constructPFChart(full_data)
    
    
    # get subset of data based on frequency
    #print(price)
    
#    start_index = 0
#    end_index = len(full_data['date'])
    
#    start_day = date2Days(start_date)
#    end_day = date2Days(end_date)
    # need to get the start and end index
#    for i in range(len(full_data['date'])):
#        if start_day < date2Days(full_data.iloc[i]['date']):
#            start_index = i-1
#            break
#    if start_index == -1:
#        start_index = 0
        
#    for i in range(start_index, len(full_data['date'])):
#        if end_day < date2Days(full_data.iloc[i]['date']):
#            end_index = i
#            break
#    if start_index == 0:
#        start_index = 1
    # all i really need is the date to use as my query
#     query_data = pd.DataFrame(full_data.iloc[getFrequencyRange(full_data, frequency, start_index, end_index)],
#                               columns=['date','high','low','close'])
 #   print(query_data)
    full_data['asset'] = asset 
    return get_ratings(pf_data, full_data)


# In[160]:


#df = pd.read_csv('data/STZ.csv')


# In[161]:


#df


# In[162]:


#d = get_PF_Ratings(df,"STZ")


# In[164]:


#pf_chart = constructPFChart(df)
#d[200:]


# In[70]:


#len(pf_chart) #150
#pf_chart[211]


# In[71]:


#pf_chart[300]


# In[ ]:





# In[77]:


#df = pd.read_csv('data/V.csv')


# In[84]:


#d = get_PF_Ratings('05-02-2008', '01-01-2012', 'd', "V",df)


# In[ ]:





# In[86]:


#d[0:50]


# In[1899]:


#d[800:850]
#import os
#cwd = os.getcwd()
#print(cwd)

