import pandas as pd
import numpy as np
from scipy import stats
import sys


OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)

def main():
    reddit_counts = pd.read_json(sys.argv[1], lines=True)
    reddit_counts['date'] = pd.to_datetime(reddit_counts['date'])
    reddit_counts = reddit_counts[(reddit_counts['subreddit'] == 'canada') & 
                                  (reddit_counts['date'].dt.year.isin([2012, 2013]))]
    reddit_counts['is_weekend'] = reddit_counts['date'].dt.weekday.isin([5, 6])

    weekday_counts = reddit_counts[reddit_counts['is_weekend'] == False]['comment_count']
    weekend_counts = reddit_counts[reddit_counts['is_weekend'] == True]['comment_count']

    initial_ttest_p = stats.ttest_ind(weekday_counts, weekend_counts).pvalue
    initial_weekday_normality_p = stats.normaltest(weekday_counts).pvalue
    initial_weekend_normality_p = stats.normaltest(weekend_counts).pvalue
    initial_levene_p = stats.levene(weekday_counts, weekend_counts).pvalue

    transformed_weekday_counts = np.sqrt(weekday_counts)
    transformed_weekend_counts = np.sqrt(weekend_counts)

    transformed_weekday_normality_p = stats.normaltest(transformed_weekday_counts).pvalue
    transformed_weekend_normality_p = stats.normaltest(transformed_weekend_counts).pvalue
    transformed_levene_p = stats.levene(transformed_weekday_counts, transformed_weekend_counts).pvalue

    reddit_counts['week_number'] = reddit_counts['date'].dt.isocalendar().week
    reddit_counts['year_number'] = reddit_counts['date'].dt.isocalendar().year
    weekly_counts = reddit_counts.groupby(['year_number','week_number', 'is_weekend'])['comment_count'].mean().reset_index()

    weekly_weekday_counts = weekly_counts[weekly_counts['is_weekend'] == False]['comment_count']
    weekly_weekend_counts = weekly_counts[weekly_counts['is_weekend'] == True]['comment_count']

    weekly_ttest_p = stats.ttest_ind(weekly_weekday_counts, weekly_weekend_counts).pvalue
    weekly_weekday_normality_p = stats.normaltest(weekly_weekday_counts).pvalue
    weekly_weekend_normality_p = stats.normaltest(weekly_weekend_counts).pvalue
    weekly_levene_p = stats.levene(weekly_weekday_counts, weekly_weekend_counts).pvalue

    utest_p = stats.mannwhitneyu(weekday_counts, weekend_counts).pvalue

    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=initial_ttest_p,
        initial_weekday_normality_p=initial_weekday_normality_p,
        initial_weekend_normality_p=initial_weekend_normality_p,
        initial_levene_p=initial_levene_p,
        transformed_weekday_normality_p=transformed_weekday_normality_p,
        transformed_weekend_normality_p=transformed_weekend_normality_p,
        transformed_levene_p=transformed_levene_p,
        weekly_weekday_normality_p=weekly_weekday_normality_p,
        weekly_weekend_normality_p=weekly_weekend_normality_p,
        weekly_levene_p=weekly_levene_p,
        weekly_ttest_p=weekly_ttest_p,
        utest_p=utest_p,
    ))

if __name__ == '__main__':
    main()