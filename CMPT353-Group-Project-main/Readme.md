Required packages/libraries:
Pandas,
Numpy,
Matplotlib,
scikit-learn,
SciPy,
statsmodels,
seaborn,
tensorflow

data_since_1977.7z are the entire datasets for the LabourForce data.
LabourForce2023 records only up to June 2023
covid19-download.csv is the entire dataset for the pandemic data

All the source code in this project are provided in the folder 'Source Code'
The 14100287-eng.zip, 14100287-SDMX.zip, and covid19-download.csv are in the folder 'Resource Files'
All the output we produce in data processing and data cleaning, and data analyzing are provided in the folder 'Result Files'

How to get all results and generate files in the 'Result Files' folder from scratch(code that uses models with randomized algorithms will produce slightly different files):
1. Ensure that 'python' command invokes python 3.10, or replace each 'python' command below with one that does so, for example 'python3'
2. Ensure all required packages/libraries are installed
3. Navigate to the 'Resource Files' folder. Unzip 'data_since_1977.7z' into 'data_since_1977.csv', leave it in the 'Resource Files' folder
4. Navigate to the 'Source Code' folder
5. Run 'python combine-csv.py' to get 'Result Files/combined.csv'
6. Run 'python reformat_combined.py' to get 'combined_reformatted.csv'
7. Run 'python add_total.py' to get 'combined_reformatted_total_included.csv'
8. Run "python 'Clean&Visualization.py'" to get the files starting with 'unempl_' and 'Unempl_'
9. Run 'python append_covid_data.py' to get 'covid_and_employment_total_included.csv'
10. Run 'python augment_national_covid.py' to get 'covid_and_employment_augmented_national_covid.csv'
11. Run 'python Unempl_Sex_Analysis.py' to get files 'Unemployment_Summary_Male.csv', 'Unemployment_Summary_Male.csv' and 'Sex_Compar.png'. It will also print a pvalue for difference in trend of male and female unemployment
12. Run 'python Combine_male_female.py' to get 'Unemployment_rate_AllGender.csv'
13. Run 'python Before_After_Comparision.py' to get files 'test_results.csv' and 'Unemployment_rate_boxplot.png'
14. Run 'python clean_data.py' to get 'un_1997.csv'
15. Run 'python covid_caseRate.py'. Instead of saving to file, it will show the graph 'Rate of COVID-19 Cases by Province', and also print out the pvalue for ttest_ind between Alberta and Yukon's weekly cases
16. Run 'python GEO_comparision.py'. Instead of saving to file, it will show the graph 'Unemployment rate In Newfoundland and Labrador and Sascatchewan', as well as showing the pvalue for Mann-Whitney U test of these two data
17. Run 'python polynomial_fits_driver_code.py'. It will invoke .py files 'unemployment_rate_fit.py', 'during_pandemic_fit.py' and 'augmented_fit.py', and generate all files in subdirectories 'augmented', 'fit_results', 'pandemic' and 'usual' of the folder 'Result Files'
18. Run 'python ML-DL.py' to get file 'DNN_results.csv'
19. Run 'python ML-KNN.py' to get files 'KNN_results.csv' and 'KNN_results_figure.png'
20. Run 'python ML-RF.py' to get files 'RF_results.csv' and 'RF_results_figure.png'
21. Run 'python Trend_Compare.py' to get Trend_Compar.png

The 'Result Files' Folder contains all the information we used in our report, aside from the plots showed and the outputs printed to the console in the steps above.
The Folders 'Eric', 'Gary', and 'Isaac' were created for the convenience of code management,
all the files in these folders have been duplicated in the three folders I mentioned above based on their function.

We coded on another repository, then migrated the repository to github.sfu.ca, therefore some commit are done with our other accounts:
Commits by 'ericzhouhy' are commits by Huanyu Zhou, student number 301417467, Computing ID ericzhouhy
Commits by 'Is Ding' are commits by Isaac Ding, student number 301425524, Computing ID ida8
