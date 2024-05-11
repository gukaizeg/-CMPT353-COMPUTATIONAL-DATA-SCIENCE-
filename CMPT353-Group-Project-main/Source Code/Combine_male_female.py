import pandas as pd

# Assuming your data is in a CSV file called 'your_data.csv', you can read it into a pandas DataFrame
df = pd.read_csv('../Result Files/combined.csv')

# Step 1: Filter rows with "Labour force characteristics" as "Population" and sum the "VALUE" by "REF_DATE" and "GEO"
population_df = df[df['Labour force characteristics'] == 'Population']
population_grouped = population_df.groupby(['REF_DATE', 'GEO'])['VALUE'].sum().reset_index()
population_grouped.rename(columns={'VALUE': 'Population'}, inplace=True)

# Step 2: Filter rows with "Labour force characteristics" as "Unemployment" and sum the "VALUE" by "REF_DATE" and "GEO"
unemployment_df = df[df['Labour force characteristics'] == 'Unemployment']
unemployment_grouped = unemployment_df.groupby(['REF_DATE', 'GEO'])['VALUE'].sum().reset_index()
unemployment_grouped.rename(columns={'VALUE': 'Unemployment'}, inplace=True)

# Step 3: Merge population and unemployment DataFrames and calculate the new value
combined_df = pd.merge(population_grouped, unemployment_grouped, on=['REF_DATE', 'GEO'])
combined_df['Unemployment rate'] = combined_df['Unemployment'] / combined_df['Population']

combined_df.to_csv('../Result Files/Unemployment_rate_AllGender.csv')