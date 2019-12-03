#if len(sys.argv) < 4:
#    print_desc()

import sys
import argparse
import os
from selenium import webdriver
import pandas as pd
import random
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time
from io import StringIO

#print("/Users/johnnyd/Downloads/chromedriver")
# argument passing: START

parser = argparse.ArgumentParser(description='An automated system for determining whether to buy or sell stocks based on P&F and moving averages charts.')

def valid_path(filename):

    if os.path.exists(filename):
        if not valid_path.counter == 2:
            parser.error("need to pass args in order, i.e. -sc username password path/to/chromedriver")
        else:
            valid_path.counter += 1
            return filename
    else:
        if valid_path.counter == 2:
            parser.error("incorrect filename")
        else:
            valid_path.counter += 1
            return filename
valid_path.counter = 0

def valid_file(filename):

    if os.path.exists(filename):
        return filename
    else:
        parser.error("incorrect filename")

def valid_number(val):
    if 0 <= int(val) and int(val) < 500:
        return int(val)
    else:
        parser.error("need a valid integer between 0 and 499")


parser.add_argument('-f','--file', type=valid_file, default=None, dest='file', help='file containing tickers')
parser.add_argument('-sp','--SP500', type=valid_number, default=None, dest='SP500', help='number of random tickers requested from S&P 500')
parser.add_argument('-av','--alpha_vantage', default=None, dest='alpha_vantage', help='alpha vantage api key used to get historical stock data from tickers')
parser.add_argument('-sc','--stock_charts', nargs=3, default=None, dest='stock_charts', \
                    type=valid_path, metavar=("username", "password", "path/to/chromedriver"), \
                    help='username and password for stockcharts.com and path to chromedriver')
args = parser.parse_args()

if not ((args.alpha_vantage==None and not args.stock_charts==None) or (not args.alpha_vantage==None and args.stock_charts==None)):
    parser.error("need to supply exclusively either s&p amount or stockcharts.com username, password, and path to chromedriver")

if not ((args.file==None and not args.SP500==None) or (not args.file==None and args.SP500==None)):
    parser.error("need to supply exclusively either a file with tickers or integer of number of requested tickers from S&P 500")

# argument passing: END

def dataSP(amount):

    data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    table = data[0]

    data_cleaned = table[['Symbol','GICS Sector','GICS Sub Industry','CIK','Founded']]

    tickers = data_cleaned['Symbol'].tolist()
    # get n random stocks from S&P
    rand_vals = random.sample(range(0,500), amount)
    stocks50 = []

    for i in rand_vals:
        stocks50.append(tickers[i])

    return stocks50

tickFile = None
tickAmount = None
userName = None
passWord = None
cdPath = None
av_key = None

# get tickers from S&P 500 or file
tickers = []

if args.file:
    tickFile = args.file
    with open(tickFile) as f:
        for tick in f.readlines():
            tickers.append(tick.strip())
if args.SP500:
    tickAmount = args.SP500
    tickers =  dataSP(tickAmount)
if args.stock_charts:
    userName = args.stock_charts[0]
    passWord = args.stock_charts[1]
    cdPath = args.stock_charts[2]
if args.alpha_vantage:
    av_key = args.alpha_vantage

if not os.path.isdir('data'):
    os.mkdir('data')

def convert_raw_sc_data(fileName):                                                                                                                                                     
    data = None
    with open('raw_data/'+fileName,'r') as f:
        data = f.read()

    sp = data.split('\n')

    # get ticker name
    ticker = sp[0].split(',')[0]

    # so hacky
    features = sp[1].split('      ')[1:6]
#   print(features)
    date_ = []
    open_ = []
    high_ = []
    low_ = []
    close_ = []

    for line in reversed(sp[3:]):
        try:
            values = line.split()
            date_.append(values[1])
            open_.append(values[2])
            high_.append(values[3])
            low_.append(values[4])
            close_.append(values[5])
        except:
            continue

    df = {'date' : date_, 'open' : open_, 'high' : high_, 'low' : low_, 'close' : close_}
    df = pd.DataFrame(data=df)
    df.to_csv('data/'+ticker+'.csv')


# get the data from stockcharts.com
def scData():

    browser = webdriver.Chrome(executable_path = cdPath)
    browser.get('http://www.stockcharts.com/')
    python_button = browser.find_element_by_id("nav-loginBtn")
    python_button.click()

    username = browser.find_element_by_id("form_UserID")
    password = browser.find_element_by_name("form_UserPassword")

    username.send_keys(userName)
    password.send_keys(passWord)

    browser.find_element_by_css_selector('.btn.btn-lg.btn-success.btn-block.login-panel-button').click()

    browser.find_element_by_partial_link_text('Charts & Tools').click()

    browser.find_element_by_xpath('//*[@id="pnfsearch"]/div/span/button').click()

    # this is where we get data from each ticker
    for ticker in stocks50:

        input_asset = browser.find_element_by_xpath('//*[@id="SCForm1-ticker"]')
        input_asset.send_keys(ticker)
        browser.find_element_by_xpath('//*[@id="SCForm1"]/div[1]/div/table/tbody/tr[1]/td[3]/input').click()
        browser.find_element_by_xpath('//*[@id="sharpCharts2"]/div[1]/div/table/tbody/tr/td[4]/a').click()
        data=browser.find_element_by_tag_name("pre").text

        with open("raw_data/"+ticker+".txt", "w") as f:
            f.write(data)       
        browser.find_element_by_xpath('//*[@id="navbar-menuCollapse"]/ul[1]/li[1]/a').click()
        browser.find_element_by_xpath('//*[@id="pnfsearch"]/div/span/button').click()
    browser.quit()
    
    for f in os.listdir("raw_data"): 
        convert_raw_sc_data(f)

def avData():
    """
    Get daily adjusted data and combine them into one dataframe
    """


    ts = TimeSeries(key=av_key.strip(), output_format= 'pandas')

    csvFiles = [] # Define an empty list to contain dataframes
    t = 0 # time counter
    print(tickers)

    for ticker in tickers:

        try:
            data, meta_data = ts.get_daily_adjusted(symbol=ticker.strip(), outputsize='full') # Download the daily data
        except:
            print(ticker + " is not available on alpha vantage")
            continue
        print(ticker)
        t = t + 1

        data.drop(['1. open','4. close','6. volume','7. dividend amount', '8. split coefficient'],axis=1, inplace=True)
        #data.insert(1, 'company' ,ticker)
        data.rename(columns = {'2. high':'high','3. low':'low','5. adjusted close':'close'}, inplace = True)
        
        # Add the dataframe to the list
        if t%5 == 0:
            print("Pause the downloading...")
            time.sleep(60)
            print("Resume the downloading...")
            
        csvFiles.append("data/" +ticker + '.csv')
        data.to_csv(csvFiles[-1])

# get data from alpha vantage or stock charts
if av_key:
    avData()
else:
    scData()
