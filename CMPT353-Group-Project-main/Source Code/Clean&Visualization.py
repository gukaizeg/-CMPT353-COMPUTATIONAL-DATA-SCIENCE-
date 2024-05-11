
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
df = pd.read_csv('../Resources Files/data_since_1977.csv')
df['REF_DATE'] = pd.to_datetime(df['REF_DATE'], format='%Y-%m')

# Keep only unemployment rate data
unempl_rate_data = df[(df['Labour force characteristics'] == 'Unemployment rate')]
unempl_rate_data = unempl_rate_data[(unempl_rate_data['Age group'] == '15 years and over')]
unempl_rate_data = unempl_rate_data[(unempl_rate_data['Data type'] == 'Seasonally adjusted')]
unempl_rate_data = unempl_rate_data[(unempl_rate_data['Statistics'] == 'Estimate')]
unempl_rate_data = unempl_rate_data.sort_values(by='REF_DATE')
unempl_male = unempl_rate_data[unempl_rate_data['Sex'] == 'Males']
unempl_female = unempl_rate_data[unempl_rate_data['Sex'] == 'Females']
unempl_both_sexs = unempl_rate_data[unempl_rate_data['Sex'] == 'Both sexes']
columns_to_drop = ['DGUID', 'Labour force characteristics',  'Age group', 'Statistics', 'Data type', 'UOM', 'UOM_ID', 'SCALAR_FACTOR', 'SCALAR_ID', 'VECTOR', 'COORDINATE', 'STATUS', 'SYMBOL', 'TERMINATED', 'DECIMALS']
unempl_rate_data.drop(columns=columns_to_drop, inplace=True)
unempl_rate_data.rename(columns={'VALUE': 'Unemployment Rate'}, inplace=True)

# Out put the data for whole table, and different sexes
unempl_rate_data.to_csv('../Result Files/unempl_rate_since_1977.csv', index=False)
unempl_male = unempl_rate_data[unempl_rate_data['Sex'] == 'Males']
unempl_female = unempl_rate_data[unempl_rate_data['Sex'] == 'Females']
unempl_both_sexs = unempl_rate_data[unempl_rate_data['Sex'] == 'Both sexes']
unempl_male.to_csv('../Result Files/unempl_male.csv', index=False)
unempl_female.to_csv('../Result Files/unempl_female.csv', index=False)
unempl_both_sexs.to_csv('../Result Files/unempl_both_sex.csv', index=False)

# Plot the data for males and females
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
grouped_male = unempl_male.groupby('GEO')
grouped_female = unempl_female.groupby('GEO')
for geo, group_data in grouped_male:
    ax1.plot(group_data['REF_DATE'], group_data['Unemployment Rate'],label=geo)
ax1.set_title('Plot Grouped by GEO for Males')
for geo, group_data in grouped_female:
    ax2.plot(group_data['REF_DATE'], group_data['Unemployment Rate'],label=geo)
ax2.set_title('Plot Grouped by GEO for Females')
plt.xlabel('Date')
ax1.set_ylabel('Value')
ax2.set_ylabel('Value')
plt.legend() 
plt.xticks(rotation=45)
plt.tight_layout() 
plt.savefig('../Result Files/Umempl_Sex_compar.png')
plt.close()