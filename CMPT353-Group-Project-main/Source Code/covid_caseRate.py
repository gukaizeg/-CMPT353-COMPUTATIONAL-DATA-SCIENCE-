import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
import scipy.stats as stats
import statsmodels.api as sm

df = pd.read_csv('../Resources Files/covid19-download.csv')

df = df.dropna(subset=['ratecases_last7'])

# Convert 'date' column to datetime type in pandas for proper plotting
df['date'] = pd.to_datetime(df['date'])

# Group the data by 'prnameFR' and calculate the average rate of cases per day for each group
grouped_df = df.groupby(['prname', pd.Grouper(key='date', freq='M')])['ratecases_last7'].mean().reset_index()

# Create a plot with multiple lines, one for each province
plt.figure(figsize=(12, 6))  # Adjust the figure size as needed

unique_provinces = df['prname'].unique()

for province in unique_provinces:
    data_for_province = grouped_df[grouped_df['prname'] == province]
    plt.plot(data_for_province['date'], data_for_province['ratecases_last7'], label=province)

# Format x-axis to show only the month
plt.gca().xaxis.set_major_locator(MonthLocator())
plt.gca().xaxis.set_major_formatter(DateFormatter('%b %Y'))

plt.xlabel('Date')
plt.ylabel('Rate of Cases (Last 7 days)')
plt.title('Rate of COVID-19 Cases by Province')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

Alberta = df[df['prname'] == 'Alberta']['ratecases_last7']
Yukon = df[df['prname'] == 'Yukon']['ratecases_last7']

# Perform the t-test
t_stat, p_value = stats.ttest_ind(Alberta, Yukon)

print(p_value)

alpha = 0.05
if p_value < alpha:
    print("Reject the null hypothesis. There is a significant difference between the groups.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference between the groups.")


plt.close()
