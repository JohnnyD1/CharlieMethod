#!/usr/bin/env python
# coding: utf-8

# so we need date, buy, rating, and then sell on rating
import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(description='Test the Woo Rating System given data, shares, etc to determine if rating method is sound.', \
            epilog='Example:\n\tpython BuySellTesting.py -f results/CMS_output.csv -pfb 1 -pfs 2 3 4 -smab 1 6 -smas 2 3 4 5 -sh_amt 10 -bf 0')

def valid_file(filename):

    if os.path.exists(filename):
        return filename
    else:
        parser.error("incorrect filename")

def valid_pf_number(val):
    try:
        if 0 < int(val) and int(val) <= 4:
            return int(val)
    except:
        None
    parser.error("must provide valid integer between 1 and 4")

def valid_sma_number(val):
    try:
        if 0 < int(val) and int(val) <= 6:
            return int(val)
    except:
        None
    parser.error("must provide a valid integer between 1 and 6")

def valid_shares_amount(val):
    try:
        if int(val) > 0:
            return int(val)
    except:
        parser.error("must provide a valid positive integer")
        
def valid_buy_fee(val):
    try:
        if float(val) >= 0:
            return float(val)
    except:
        parser.error("must provide a valid nonegative float")
        
parser.add_argument('-f','--file', type=valid_file, nargs=1, default=None, dest='file', required=True, \
    help='data csv file from results/')
parser.add_argument('-pfb','--pf_buy', type=valid_pf_number, nargs='*', default=None, required=True, \
    metavar='P&F buy rating', dest='pf_buy', help='P&F rating to buy on (1-4)')
parser.add_argument('-pfs','--pf_sell', type=valid_pf_number, nargs='*', default=None, required=True, \
    metavar='P&F sell rating', dest='pf_sell', help='P&F rating to sell on (1-4)')
parser.add_argument('-smab','--sma_buy', type=valid_sma_number, nargs='*', default=None, required=True, \
    dest='sma_buy', metavar='SMA buy rating',help='Simple Moving Averages rating to buy on (1-6)')
parser.add_argument('-smas','--sma_sell', type=valid_sma_number, nargs='*', default=None, required=True, \
    dest='sma_sell', metavar='SMA sell rating', help='Simple Moving Averages rating to sell on (1-6)')
parser.add_argument('-sh_amt', '--share_amount', type=valid_shares_amount, nargs=1, default=None, required=True, \
    dest='share_amount', metavar='share amount', help='Number of shares you want to buy')
parser.add_argument('-bf', '--buy_fee', type=valid_buy_fee, nargs=1, default=None, required=True, \
    dest='buy_fee', metavar='buy fee', help='total extra fee involved with buying shares')

args = parser.parse_args()

buy_rating_pf = args.pf_buy
buy_rating_ma = args.sma_buy
sell_rating_pf = args.pf_sell
sell_rating_ma = args.sma_sell

# once we buy, we don't buy more until we sell
# this can be an added feature in the next version
def buy_sell_test(df, pf_buy, ma_buy, pf_sell, ma_sell, shares, fees=0.0):
    buy = True

    res = []
    temp = []
#    print(cur_asset)
    for index, row in df.iterrows():

        if buy:
            if row['PF_rating'] in pf_buy and row['SMA_rating'] in ma_buy:
                temp.append([row['asset'], row['date'], row['close'], shares, fees, (row['close']*shares+fees)])
                buy = False
        elif (row['PF_rating'] in pf_sell or row['SMA_rating'] in ma_sell):
            temp.append([row['date'], row['close'], (shares*row['close'])-temp[-1][5], (shares*row['close'])/temp[-1][5]])
            res.append(temp[-2]+temp[-1])
            buy = True
            temp = []
    cols = ['asset','date_bought','close_bought','shares','fee','amt_bought','date_sold','close_sold','profit','percent_returns']
    df = pd.DataFrame(res,columns = cols)
    return df

df = pd.read_csv(args.file[0])
res = buy_sell_test(df, buy_rating_pf, buy_rating_ma, sell_rating_pf, sell_rating_ma, args.share_amount[0], args.buy_fee[0])

if len(res.index) == 0:
    print("combination of buy/sell ratings does not exist")
    exit()

# if we wanted to save to csv
with open('results/' + res.iloc[0][0] + '_buy_sell_tests.csv','w') as f:
    res.to_csv(f)

# sorting by date
#df_sorted = pd.DataFrame(sorted(res.values, key=lambda x: x[1].split('-')[::-1]), columns=res.columns)

df_sorted = res.sort_values(by=['date_bought'])

dates_bought = set()
dates_sold = set()
for index, row in df_sorted.iterrows():
    dates_bought.add(row['date_bought'].split('-')[0])
    dates_sold.add(row['date_sold'].split('-')[0])
#print(dates_bought)
#print(dates_sold)

year_start = ""
while True:
    print ("choose starting year:")
    for date in sorted(dates_bought):
        print(date)
    year_start = input()
    if not year_start in dates_bought:
        print("year is not valid")
    else:
        break

year_end = ""
while True:
    print ("choose ending year greater or equal to starting year:")
    for date in sorted(dates_sold):
        print(date)
    year_end = input()
    if year_end in dates_sold and year_end >= year_start:
        break
    else:
        print("year is not valid")


idx_start = None
idx_end = None
for index, row in df_sorted.iterrows():
    if year_start in row['date_bought']:
        year_start = row['date_bought']
        idx_start = index
        break

found = False
for index, row in df_sorted.iterrows():
    
    if year_end in row['date_sold']:
        found = True
    else:
        if found:
            year_end = df_sorted['date_sold'][df_sorted.index[index-1]]
            idx_end = index
            break

if not '-' in year_end:
    year_end = df_sorted['date_sold'][df_sorted.index[len(df_sorted.index)-1]]
    idx_end = len(df_sorted.index)

tot_prof = df_sorted[idx_start:idx_end]['profit'].sum()
print ("total simulated profit in USD: " + str(tot_prof))


tot_invest = df_sorted[idx_start:idx_end]['amt_bought'].sum()
print("total cost of buying stocks: " + str(tot_invest))

print("percentage gain: " + str((tot_invest+tot_prof)/tot_invest))

