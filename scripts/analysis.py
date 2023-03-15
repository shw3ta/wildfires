import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# goal one: produce the log-log plot for one file
# goal two: extract slope of regression line

with open('../logfiles/logfile_0.008.json', 'r+') as f:
	data = json.load(f)

area_per_fire_dict = data['A_f_per_fire']

# make a dataframe of it
df = pd.DataFrame.from_dict(area_per_fire_dict, orient='index')

# histogram of number of fires with a certain area
count, div = np.histogram(df[0], bins=1000)
# print(count, div)
df.hist(bins=1000)
# plt.show()

# use the divs to add a class column and then make a log log plot of it after sorting it
dig = np.digitize(df[0], div, right=True)
# print(dig)
df['binned to fq'] =  dig
df = df.sort_values('binned to fq', ascending=False).reset_index(drop=True)
print(df)