#!/usr/bin/env python
# coding: utf-8



import sys
from MovingAveragesRating import get_MA_Ratings
from PointFigureRating_HLv3 import get_PF_Ratings
import pandas as pd
import os
import csv


files = os.listdir("data")
#print(files)
df = None
#outputfile = 'results/output.csv'
files = ['AAPL.csv']
outputfile = 'results/' + files[0].split('.')[0] + '_output.csv'

features = ['date','SMA_rating','PF_rating','high','close','asset','returns']
with open(outputfile,'a') as f:
    writer = csv.writer(f)
    writer.writerow(features)

# here's the magic
inc = 1

for fl in files:

    df_temp = pd.read_csv('data/'+fl)
    ma_results = get_MA_Ratings(df_temp)
#    print(ma_results)
    pf_results = get_PF_Ratings(df_temp,os.path.splitext(fl)[0])
#    print(pf_results)
    ma_results['PF_rating'] = pf_results['PF_rating']

    ma_results['high'] = pf_results['high']
    ma_results['close'] = pf_results['close']
    ma_results['asset'] = os.path.splitext(fl)[0]
    ma_results['returns'] = ma_results['close'].diff()
    with open(outputfile,'a') as f:
        ma_results.to_csv(f, header=False)
        
    #results.append(ma_results)
    print(str(inc)+' '+ma_results['asset'].iloc[0]+' done')
    inc += 1
 
