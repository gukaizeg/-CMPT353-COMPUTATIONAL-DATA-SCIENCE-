import pandas as pd

df = pd.read_csv('../Result Files/unempl_rate_since_1977.csv')

df_filtered = df[df['Sex'] == 'Both sexes']

df_filtered.to_csv('../Result Files/un_1997.csv', index=False)
