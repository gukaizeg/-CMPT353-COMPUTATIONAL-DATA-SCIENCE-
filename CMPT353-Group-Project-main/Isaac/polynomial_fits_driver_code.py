import pandas as pd
import unemployment_rate_fit as usual
import during_pandemic_fit as during_pandemic
import augmented_fit as augmented
import os
names = ['Alberta',
         'British Columbia',
         'Canada',
         'Manitoba',
         'New Brunswick',
         'Newfoundland and Labrador',
         'Nova Scotia',
         'Ontario',
         'Prince Edward Island',
         'Quebec',
         'Saskatchewan'
]
os.makedirs('./usual', exist_ok = True)
os.makedirs('./pandemic', exist_ok = True)
os.makedirs('./augmented', exist_ok = True)
os.makedirs('./fit_results', exist_ok= True)
usual_results_df = pd.DataFrame(columns=['GEO',
                                         'prediction with covid cases pvalue',
                                         'prediction with covid deaths pvalue',
                                         'predictions with both score',
                                         'polynomial regression of both score'])
during_pandemic_df = usual_results_df
augmented_df = pd.DataFrame(columns = ['GEO',
                                       'multilinear prediction',
                                       'polynomial prediction'])
for name in names:
    usual_result = usual.fit(name)
    usual_results_df = pd.concat([usual_results_df, usual_result],
                                 axis = 0,
                                 ignore_index= True)
    during_pandemic_result = during_pandemic.fit(name)
    during_pandemic_df = pd.concat([during_pandemic_df, during_pandemic_result],
                                   axis = 0,
                                   ignore_index = True)
    augmented_result = augmented.fit(name)
    augmented_df = pd.concat([augmented_df, augmented_result],
                             axis = 0,
                             ignore_index = True)

usual_results_df.to_csv('./fit_results/usual_polynomial_fits.csv', index = False)
during_pandemic_df.to_csv('./fit_results/during_pandemic_polynomial_fits.csv', index = False)
augmented_df.to_csv('./fit_results/augmented_fits.csv', index = False)
