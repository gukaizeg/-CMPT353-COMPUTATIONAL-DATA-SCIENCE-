import pandas as pd


totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])


annual_totals = totals.sum(axis=1)
city_with_least_precipitation = annual_totals.idxmin()
monthly_totals = totals.sum(axis=0)
monthly_counts = counts.sum(axis=0)
average_monthly_precipitation = monthly_totals / monthly_counts
city_totals = totals.sum(axis=1)
city_counts = counts.sum(axis=1)
average_city_precipitation = city_totals / city_counts
print("City with lowest total precipitation:")
print(city_with_least_precipitation)
print("Average precipitation in each month:")
print(average_monthly_precipitation)
print("Average precipitation in each city:")
print(average_city_precipitation)