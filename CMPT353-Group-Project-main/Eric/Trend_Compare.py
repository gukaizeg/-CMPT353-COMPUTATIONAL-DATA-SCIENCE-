import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu


unempl_male = pd.read_csv('unempl_male.csv')
unempl_female = pd.read_csv('unempl_female.csv')

merged_data = pd.merge(unempl_male, unempl_female, on=['REF_DATE', 'GEO'], suffixes=('_male', '_female'))

merged_data.rename(columns={'Unemployment Rate_male': 'Male', 'Unemployment Rate_female': 'Female'}, inplace=True)

merged_data['REF_DATE'] = pd.to_datetime(merged_data['REF_DATE'])

merged_data.set_index('REF_DATE', inplace=True)

merged_data_monthly = merged_data.resample('MS').mean()

# Decomposition
result_male = sm.tsa.seasonal_decompose(merged_data_monthly['Male'], model='additive')
result_female = sm.tsa.seasonal_decompose(merged_data_monthly['Female'], model='additive')

# Plot the trend component for males and females
plt.figure(figsize=(10, 6))
plt.plot(result_male.trend, label='Male Trend')
plt.plot(result_female.trend, label='Female Trend')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate')
plt.title('Trend Component Comparison for Male and Female')
plt.legend()
plt.savefig('Trend_Compar.png')
