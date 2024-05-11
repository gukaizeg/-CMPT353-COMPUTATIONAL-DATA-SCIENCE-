import sys
import pandas as pd
from scipy.stats import mannwhitneyu, chi2_contingency

OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)

def main():
    searchdata_file = sys.argv[1]

    # Load the data
    data = pd.read_json(searchdata_file, orient='records', lines=True)

    # Create groups for A/B testing
    groupA = data[data.uid % 2 == 0]  # Old design
    groupB = data[data.uid % 2 != 0]  # New design

    # Q1: Did more/less users use the search feature?
    contingency = pd.crosstab(data.uid % 2, data.search_count > 0)
    _, more_users_p, _, _ = chi2_contingency(contingency)

    # Q2: Did users search more often?
    _, more_searches_p = mannwhitneyu(groupA.search_count, groupB.search_count)

    # Repeat for instructors only
    instructors = data[data.is_instructor]
    groupA_instr = instructors[instructors.uid % 2 == 0]  # Old design
    groupB_instr = instructors[instructors.uid % 2 != 0]  # New design

    # Q3: Did more/less instructors use the search feature?
    contingency_instr = pd.crosstab(instructors.uid % 2, instructors.search_count > 0)
    _, more_instr_p, _, _ = chi2_contingency(contingency_instr)

    # Q4: Did instructors search more often?
    _, more_instr_searches_p = mannwhitneyu(groupA_instr.search_count, groupB_instr.search_count)

    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=more_users_p,
        more_searches_p=more_searches_p,
        more_instr_p=more_instr_p,
        more_instr_searches_p=more_instr_searches_p,
    ))

if __name__ == '__main__':
    main()
