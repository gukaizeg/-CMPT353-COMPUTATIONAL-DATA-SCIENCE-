import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv('data.csv')

model = ols('time_taken ~ C(sort_implementation)', data=data).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

print(anova_table)

if anova_table["PR(>F)"][0] < 0.05:
    tukey = pairwise_tukeyhsd(endog=data['time_taken'], groups=data['sort_implementation'], alpha=0.05)
    print(tukey)


rank = data.groupby('sort_implementation')['time_taken'].mean().sort_values()
print(rank)
