import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
import scipy.stats as stats
import statsmodels.api as sm

df = pd.read_csv('covid19-download.csv')

df = df.dropna(subset=['ratedeaths_last7'])

# Convert 'date' column to datetime type in pandas for proper plotting
df['date'] = pd.to_datetime(df['date'])
df['deathRate_7'] = df['ratedeaths_last7']/df['ratecases_last7']

# Group the data by 'prnameFR' and calculate the average rate of cases per day for each group
grouped_df = df.groupby(['prname', pd.Grouper(key='date', freq='M')])['deathRate_7'].mean().reset_index()

# Create a plot with multiple lines, one for each province
plt.figure(figsize=(12, 6))  # Adjust the figure size as needed

unique_provinces = df['prname'].unique()

for province in unique_provinces:
    data_for_province = grouped_df[grouped_df['prname'] == province]
    plt.plot(data_for_province['date'], data_for_province['deathRate_7'], label=province)

# Format x-axis to show only the month
plt.gca().xaxis.set_major_locator(MonthLocator())
plt.gca().xaxis.set_major_formatter(DateFormatter('%b %Y'))

plt.xlabel('Date')
plt.ylabel('Rate of Death (Last 7 days)')
plt.title('Rate of COVID-19 Cases by Province')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()