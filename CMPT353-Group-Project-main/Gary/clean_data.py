import pandas as pd

df = pd.read_csv('unempl_rate_since_1977.csv')

df_filtered = df[df['Sex'] == 'Both sexes']

df_filtered.to_csv('un_1997.csv', index=False)
