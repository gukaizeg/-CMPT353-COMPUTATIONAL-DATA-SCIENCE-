import pandas as pd

data = pd.read_csv('../combined.csv')
data['descriptor'] = data['Labour force characteristics']

# this filters the unique combinations of columns ['REF_DATE', 'GEO', 'DGUID', 'UOM']
indices = ['REF_DATE', 'GEO']
indices_val = ['REF_DATE', 'GEO', 'VALUE']
indices_val_sex = ['REF_DATE', 'GEO', 'UOM', 'Sex', 'VALUE']
reformatted = data[indices].groupby(indices) \
                       .size() \
                       .reset_index() \
                       [indices]

pop = data[data['descriptor'] == 'Population'][indices_val_sex]
labour_force = data[data['descriptor'] == 'Labour force'][indices_val_sex]
fulltime = data[data['descriptor'] == 'Full-time employment'][indices_val_sex]
unemploy = data[data['descriptor'] == 'Unemployment'][indices_val_sex]
unemploy_rate = data[data['descriptor'] == 'Unemployment rate'][indices_val_sex]
part_rate = data[data['descriptor'] == 'Participation rate'][indices_val_sex]
employ_rate = data[data['descriptor'] == 'Unemployment rate'][indices_val_sex]

pop_male = pop[pop['Sex'] == 'Males'][indices_val] \
           .rename(columns = {'VALUE': 'male population(1000)'})
pop_female = pop[pop['Sex'] == 'Females'][indices_val] \
           .rename(columns = {'VALUE': 'female population(1000)'})

labour_force_male = labour_force[labour_force['Sex'] == 'Males'][indices_val] \
                    .rename(columns = {'VALUE': 'male labour force(1000)'})
labour_force_female = labour_force[labour_force['Sex'] == 'Females'][indices_val] \
                      .rename(columns = {'VALUE': 'female labour force(1000)'})

fulltime_male = fulltime[fulltime['Sex'] == 'Males'][indices_val] \
                .rename(columns = {'VALUE': 'male fulltime employments(1000)'})
fulltime_female = fulltime[fulltime['Sex'] == 'Females'][indices_val] \
                  .rename(columns = {'VALUE': 'female fulltime employments(1000)'})

unemploy_male = unemploy[unemploy['Sex'] == 'Males'][indices_val] \
                .rename(columns = {'VALUE': 'male unemployed(1000)'})
unemploy_female = unemploy[unemploy['Sex'] == 'Females'][indices_val] \
                  .rename(columns = {'VALUE': 'female unemployed(1000)'})

unemploy_rate_male = unemploy_rate[unemploy_rate['Sex'] == 'Males'][indices_val] \
                     .rename(columns = {'VALUE': 'male unemployment rate(%)'})
unemploy_rate_female = unemploy_rate[unemploy_rate['Sex'] == 'Females'][indices_val] \
                       .rename(columns = {'VALUE': 'female unemployment rate(%)'})

part_rate_male = part_rate[part_rate['Sex'] == 'Males'][indices_val] \
                 .rename(columns = {'VALUE': 'male participation rate(%)'})
part_rate_female = part_rate[part_rate['Sex'] == 'Females'][indices_val] \
                   .rename(columns = {'VALUE': 'female participation rate(%)'})

employ_rate_male = employ_rate[employ_rate['Sex'] == 'Males'][indices_val] \
                   .rename(columns = {'VALUE': 'male employment rate(%)'})
employ_rate_female = employ_rate[employ_rate['Sex'] == 'Females'][indices_val] \
                     .rename(columns = {'VALUE': 'female employment rate(%)'})


reformatted = reformatted.merge(pop_male, on = indices) \
                         .merge(pop_female, on = indices) \
                         .merge(labour_force_male, on = indices) \
                         .merge(labour_force_female, on = indices) \
                         .merge(fulltime_male, on = indices) \
                         .merge(fulltime_female, on = indices) \
                         .merge(unemploy_male, on = indices) \
                         .merge(unemploy_female, on = indices) \
                         .merge(unemploy_rate_male, on = indices) \
                         .merge(unemploy_rate_female, on = indices) \
                         .merge(part_rate_male, on = indices) \
                         .merge(part_rate_female, on = indices) \
                         .merge(employ_rate_male, on = indices) \
                         .merge(employ_rate_female, on = indices)

reformatted.to_csv('../combined_reformatted.csv', index = False)