import os
from selenium import webdriver

# get list of S&P 500
 
import pandas as pd
data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
table = data[0]

data_cleaned = table[['Symbol','GICS Sector','GICS Sub Industry','CIK','Founded']]


tickers = data_cleaned['Symbol'].tolist()

# get 50 random stocks from S&P
import random
rand_vals = random.sample(range(0,500), 50)

stocks50 = []

for i in rand_vals:
	stocks50.append(tickers[i])



	
# get the data from stockcharts.com

browser = webdriver.Chrome(executable_path = "/usr/local/bin/chromedriver")
browser.get('http://www.stockcharts.com/')

python_button = browser.find_element_by_id("nav-loginBtn")
python_button.click()


username = browser.find_element_by_id("form_UserID")
password = browser.find_element_by_name("form_UserPassword")

username.send_keys("cse-woo5@buffalo.edu")
password.send_keys("ZOOM-JASON-789")

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

