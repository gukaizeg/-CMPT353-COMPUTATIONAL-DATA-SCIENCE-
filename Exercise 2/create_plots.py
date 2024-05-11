import sys
import matplotlib.pyplot as plt 
import pandas as pd


filename1 = sys.argv[1]
filename2 = sys.argv[2]

data = pd.read_csv(filename1, sep=' ', header=None, index_col=1,
                    names=['lang', 'page', 'views', 'bytes'])


sorted_data = data.sort_values(by='views', ascending=False)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)

plt.plot(sorted_data['views'].values)
plt.title('Popularity Distribution')
plt.xlabel('Rank')
plt.ylabel('Views')


data_2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1,
                    names=['lang', 'page', 'views', 'bytes'])


merged_data = pd.concat([data['views'], data_2['views']], axis=1)
merged_data.columns = ['views1', 'views2']


plt.subplot(1, 2, 2)
plt.scatter(merged_data['views1'], merged_data['views2'])
plt.xscale('log')
plt.yscale('log')
plt.title('Hourly Correlation')
plt.xlabel('Hour 1 views')
plt.ylabel('Hour 2 views')


plt.savefig('wikipedia.png')