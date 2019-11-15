# Woo Rating System
An automated system for determining whether to buy or sell stocks based on P&F and simple moving averages charts.
This idea is based off of the Woo Rating system, created by Dr. Charles Tirone.
This program will determine the ratings for up to 30 years of historical data based on the stock ticker symbols provided.
You will get a csv file with the ratings of both the P&F chart and the simple moving averages chart based on the rules specified below.
The idea is as follows: given certain combinations of ratings computed from P&F and SMA charts, one can determine if it is right to buy or sell their stock.
There are many methods for assigning ratings. I will explain one of the more basic methods, which is used here.

Point & Figure Chart
The rating rules are as follows:
1 is assigned as a rating if:
    1) the current column of boxes are X's
    2) 1 or more boxes are added to the top of the current column that are higher than the top of the most recent column of Os
2 is assigned as a rating if:
    1) The current column has switched from Xs to Os
3 is assigned as a rating if:
    1) The current column has switched from Os to Xs
4 is assigned as your rating if:
    1) The current column of boxes are Os
    2) 1 or more boxes are added to the bottom of the current column that are lower than the bottom of the most recent column of Xs

Given these rules, one approach could be to buy on a 1 and sell on a 2, 3, or 4. Or perhaps buy on a 1 and 3 and sell on a 4.

Simple Moving Averages Chart
This uses the 20, 50, and 200 day trendlines.
The rating rules are as follows:
1 is assigned as the rating if:
    1) The 20 is equal to or above the 50, and the 50 is equal to or above the 200
2 is assigned as the rating if:
    1) The 20 is below the 50, but the 20 is equal to or above the 200
3 is assigned as the rating if:
    1) The 50 is equal to or above the 200, and the 200 is above the 20
4 is assigned as the rating if:
    1) The 200 is above the 50, and the 50 is above the 20
5 is assigned as the rating if:
    1) The 200 is above the 20, and the 20 is equal to or above the 50
6 is assigned as the rating if:
    1) The 20 is equal to or above the 200, and the 200 is above the 50

Given these rules, one approach could be to buy on a 1 or a 6 and sell on any other rating.

Usage

git clone https://github.com/JohnnyD1/CharlieMethod.git
cd CharlieMethod

Need to use python 3 with the following modules installed:
    numpy
    pandas
    sys 
    datetime 
    os
    csv
    math
    argparse
    selenium or alpha_vantage.timeseries (at least 1 of the 2)
    io
    random
selenium only needs to be installed if you would like to use data from stockcharts.com. It requires a username and password, but its data is more accurate than alpha vantage. If you do not have a stockcharts account, you'll need to install alpha vantage.

run the following command:
python get_data.py <[-f FILE] [-sp SP500]> <[-av ALPHA_VANTAGE] [-sc username password path/to/chromedriver]>

The first 2 flags represent where you to acquire the stock ticker symbols. The last 2 flags represent where to get the data for those symbols.
You need to provide either a file (-f) with stock ticker symbols or you can get stocks from the S&P 500 (-sp) passing an integer to represent how many random stocks you want randomly selected from the S&P 500. Then, you can pass in either -av with your api key or -sc with your stockcharts.com username, password, and a path to the chromedriver app. 
A couple examples are given:
python get_data.py -f symbols.txt -av AXFDG123456789
python get_data.py -sp 10 -sc johnd password1 Application/chromedriver

Once you run get_data.py, a data directory will be created with the stock data that you can now use for getting the ratings. 
Run the following:
python MainModule.py
A directory called results should now be created with the historical ratings for each of the stock ticker symbols.

You also have the ability to test your rating system based on the rules given buy simulating a time period of buying and selling for a given time period.
run the following command:
python BuySellTesting.py -f FILE -pfb [P&F buy rating [P&F buy rating ...]] -pfs [P&F sell rating [P&F sell rating ...]] -smab [SMA buy rating [SMA buy rating ...]] -smas
 [SMA sell rating [SMA sell rating ...]] -sh_amt share amount -bf buy fee

Every argument is required:
    The flag -f should include one of the csv files in results/ that was created by running MainModule.py. 
    The flag -pfb should include a list (1 or more) of the ratings 1-4 for the P&F chart that you want to buy on.
    The flag -pfs should include a list of ratings (1 or more) of the ratings 1-4 for the P&F chart that you want to sell on.
    The flag -smab should include a list of ratings (1 or more) of the ratings 1-6 for the SMA chart that you want to buy on.
    The flag -smas should include a list of ratings (1 or more) of the ratings 1-6 for the SMA chart that you want to sell on.
    The flag -sh_amt should include a single integer representing how many shares you'd like to buy.
    The flag -bf should include a float representing a buying fee. If none, pass in 0 or 0.0.

A couple examples are given:
python BuySellTesting.py -f results/CMS_output.csv -pfb 1 -pfs 2 3 4 -smab 1 6 -smas 2 3 4 5 -sh_amt 10 -bf 0.0
python BuySellTesting.py -f results/AAPL_output.csv -pfb 1 2 -pfs 4 -smab 1 2 3 -smas 4 5 6 -sh_amt 120 -bf 7.55

While running BuySellTesting.py, you will be shown a column of years to choose as your starting year to buy on. After you pass in your valid starting year, you will see another column of years to end on. Obviously, you'll need to pick a year equal or greater than the year you chose as your starting year. You will see an output showing your total simulated profits, the total amount of money you spent on buy stocks, and the percentage of your gains throughout that time period.
For further analysis, a csv file will be created in results/ that will show you more info relating to your buys and sells for that time period.
