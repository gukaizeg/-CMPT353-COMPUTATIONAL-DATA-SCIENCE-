import numpy as np

data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

annual_totals = totals.sum(axis=1)

city_with_least_precipitation = np.argmin(annual_totals)

print("Row with lowest total precipitation:")
print(city_with_least_precipitation)

monthly_totals = totals.sum(axis=0)
monthly_counts = counts.sum(axis=0)

average_monthly_precipitation = monthly_totals / monthly_counts

print("Average precipitation in each month:")
print(average_monthly_precipitation)

city_totals = totals.sum(axis=1)
city_counts = counts.sum(axis=1)

average_city_precipitation = city_totals / city_counts

print("Average precipitation in each city:")
print(average_city_precipitation)

quarterly_totals = totals.reshape(totals.shape[0], -1, 3).sum(axis=2)

print("Quarterly precipitation totals:")
print(quarterly_totals)