import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
from matplotlib.ticker import MaxNLocator 
from scipy.stats import mannwhitneyu

df = pd.read_csv('../Result Files/unempl_both_sex.csv')

plt.figure(figsize=(12, 6))
# Keep only two provinces
new_df = df[df['GEO'].isin(['Newfoundland and Labrador', 'Saskatchewan'])]

# Create the plot
sns.lineplot(x='REF_DATE', y='Unemployment Rate', hue='GEO', data=new_df)

plt.title('Unemployment Rate in Newfoundland and Labrador and Saskatchewan')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate')

plt.xticks(rotation=45)

ax = plt.gca()
ax.xaxis.set_major_locator(MaxNLocator(nbins=8)) 

plt.legend()
plt.tight_layout()
plt.show()

#Print the p-value
Newfoundland = new_df[new_df['GEO']=='Newfoundland and Labrador']['Unemployment Rate']
Saskatchewan = new_df[new_df['GEO']=='Saskatchewan']['Unemployment Rate']
statistic, pvalue = mannwhitneyu(Newfoundland, Saskatchewan, alternative='two-sided')
print(pvalue)