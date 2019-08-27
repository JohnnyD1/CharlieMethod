import pandas as pd
import sys
from io import StringIO

def get_csv_data(fileName):

	data = None

	with open('stocks/'+fileName,'r') as f:
		data = f.read()


	sp = data.split('\n')
	#for line in sp:
	#	print(line)

	# get ticker name
	ticker = sp[0].split(',')[0]

	# so hacky
	features = sp[1].split('      ')[1:6]
#	print(features)
	date_ = []
	open_ = []
	high_ = []
	low_ = []
	close_ = []

#	print(features)

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

import os
for filename in os.listdir('stocks/'):
	get_csv_data(filename)
	
