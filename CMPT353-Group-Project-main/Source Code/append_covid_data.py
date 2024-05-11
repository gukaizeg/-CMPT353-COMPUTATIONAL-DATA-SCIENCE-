import pandas as pd

def reformat_date(date_str):
    newstr = date_str[0:7]
    return newstr

covid_data = pd.read_csv('../Resources Files/covid19-download.csv')
employment_data = pd.read_csv('../Result Files/combined_reformatted_total_included.csv')

covid_data = covid_data[['date', 'prname', 'numtotal_last7', 'numdeaths_last7']]
covid_data = covid_data.rename(columns = {'prname': 'GEO'})
covid_data['REF_DATE'] = covid_data['date'].map(reformat_date)
covid_data = covid_data.groupby(['GEO', 'REF_DATE']).agg({'numtotal_last7': 'sum',
                                                          'numdeaths_last7':'sum'})
covid_data = covid_data.rename(columns = {'numtotal_last7': 'covid cases',
                                          'numdeaths_last7': 'covid deaths'})

combined_data = employment_data.merge(covid_data, on = ['GEO', 'REF_DATE'], how = 'left')
combined_data = combined_data.fillna(0.0)
combined_data.to_csv('../Result Files/covid_and_employment_total_included.csv', index = False)