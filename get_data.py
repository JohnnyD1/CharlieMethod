import os
from selenium import webdriver
import pandas as pd
import random
import sys
import convert2csv
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time

if len(sys.argv) < 4:
	print ("invocation:")
	print ("	[-file <path/to/file storing tickers>] | [-sp <number of tickers>]")
	print ("	[-av] | [-sc <username> <password> <path/to/chromedriver>]")
	exit()

tickFile = ""
tickAmount = 0
userName = ""
passWord = ""
cdPath = ""
av = False

# parsing arguments
for i in range (1, len(sys.argv)):
	if sys.argv[i] == "-file":
		if i+1 < len(sys.argv) and os.path.exists(sys.argv[i+1]):
			tickFile = sys.argv[i+1]
			i += 1
		else:
			print ("missing path to file or file does not exist")
			exit()
	elif sys.argv[i] == "-sp":
		try:
			if i+1 < len(sys.argv) and int(sys.argv[i+1]) > 0 and int(sys.argv[i+1]) < 500:
				tickAmount = int(sys.argv[i+1])
				i += 1
			else:
				print ("incorrect ticker amount")
				sys.exit()
		except ValueError:
			print ("missing number of tickers")
			exit()
	elif sys.argv[i] == "-av":
		av = True
	elif sys.argv[i] == "-sc":
		if i+3 < len(sys.argv):
			userName = sys.argv[i+1]
			passWord = sys.argv[i+2]
			cdPath = sys.argv[i+3]
			i += 3
		else:
			print ("need to provide stockcharts.com username & password, and path to chromedriver")
			exit()

def dataSP(amount):
	data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	table = data[0]

	data_cleaned = table[['Symbol','GICS Sector','GICS Sub Industry','CIK','Founded']]


	tickers = data_cleaned['Symbol'].tolist()
	# get 50 random stocks from S&P
	rand_vals = random.sample(range(0,500), amount)

	stocks50 = []

	for i in rand_vals:
		stocks50.append(tickers[i])

	return tickers

# get tickers from S&P 500 or file
tickers = []
if tickAmount > 0:
	tickers =  dataSP(tickAmount)
else:
	with open(tickFile) as f:
		for tick in f.readlines():
			tickers.append(tick.strip())

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

		with open("stocks/"+ticker+".txt", "w") as f:
			f.write(data)		
		browser.find_element_by_xpath('//*[@id="navbar-menuCollapse"]/ul[1]/li[1]/a').click()
		browser.find_element_by_xpath('//*[@id="pnfsearch"]/div/span/button').click()
	browser.quit()
	
	convert2csv.run()

def avData():
	"""
	Get daily adjusted data and combine them into one dataframe
	"""
	avKey = input("Alpha Vantage key: ")
	# LZQ7F4KDJBC3QRTC
	# ts = TimeSeries(key='H59D4Y9AFHTRQ7HQ', output_format= 'pandas')
	ts = TimeSeries(key=avKey.strip(), output_format= 'pandas')

	csvFiles = [] # Define an empty list to contain dataframes
	t = 0 # time counter
	for ticker in tickers:
		print(ticker)
		t = t + 1
		data, meta_data = ts.get_daily_adjusted(symbol=ticker.strip(), outputsize='full') # Download the daily data

		data.drop(['1. open','4. close','6. volume','7. dividend amount', '8. split coefficient'],axis=1, inplace=True)
		#data.insert(1, 'company' ,ticker)
		data.rename(columns = {'2. high':'high','3. low':'low','5. adjusted close':'adj_close'}, inplace = True)
        
		# Add the dataframe to the list
		if t%5 == 0:
			print("Pause the downloading...")
			time.sleep(60)
			print("Resume the downloading...")
            
		csvFiles.append(ticker + '.csv')
		data.to_csv(csvFiles[-1])

# get data from alpha vantage
if av:
	avData()
else:
	scData()
