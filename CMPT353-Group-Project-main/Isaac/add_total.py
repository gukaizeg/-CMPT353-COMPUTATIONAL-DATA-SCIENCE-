import pandas as pd

data = pd.read_csv('../combined_reformatted.csv')
data['total population(1000)'] = data['male population(1000)'] + data['female population(1000)']
data['male pop weight'] = data['male population(1000)'] / data['total population(1000)']
data['female pop weight'] = data['female population(1000)'] / data['total population(1000)']
data['total labor force(1000)'] = data['male labour force(1000)'] + data['female labour force(1000)']
data['total fulltime employments(1000)'] = data['female fulltime employments(1000)'] + data['female fulltime employments(1000)']
data['total unemployed'] = data['male unemployed(1000)'] + data['female unemployed(1000)']
data['total unemployment rate(%)'] = (data['male unemployment rate(%)'] * data['male pop weight']) + \
                                     (data['female unemployment rate(%)'] * data['female pop weight'])
data['total participation rate(%)'] = (data['male participation rate(%)'] * data['male pop weight']) + \
                                     (data['female participation rate(%)'] * data['female pop weight'])
data['total employment rate(%)'] = (data['male employment rate(%)'] * data['male pop weight']) + \
                                     (data['female employment rate(%)'] * data['female pop weight'])

data = data.drop(columns = ['male pop weight', 'female pop weight'])
data.to_csv('../combined_reformatted_total_included.csv', index = False)