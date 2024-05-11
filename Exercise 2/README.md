# Exercise 2：Wikipedia Page Views and Dog Rates Tweet Analysis

## Overview
This repository contains the analysis of Wikipedia page views and the examination of tweet ratings from the @dog_rates Twitter account. The project is divided into two parts:
1. **Plotting Wikipedia Page Views** - Visualization of Wikipedia page view data across two different time frames.
2. **Analyzing Tweets from @dog_rates** - Analysis of dog rating trends over time to detect any grade inflation.

## Part 1: Plotting Wikipedia Page Views

### Description
This part involves generating plots to visualize the distribution of Wikipedia page views using two datasets from different hours.

### Usage
Run the script with the command below to generate plots:
```bash
python3 create_plots.py pagecounts-20190509-120000.txt pagecounts-20190509-130000.txt

Part 2: Analyzing Tweets from @dog_rates
Description
This part focuses on analyzing the trend of dog ratings over time from tweets collected from the @dog_rates Twitter account.

Data
The data is contained in dog_rates_tweets.csv, which includes timestamps and ratings extracted from the tweets.

Usage
Open the dog-rates.ipynb Jupyter notebook and execute the cells to perform the analysis and generate the plots.

Analysis Steps
Data Loading and Cleaning: Load tweets, extract valid ratings, and remove outliers.
Time Parsing: Convert tweet timestamps into datetime objects for analysis.
Trend Analysis: Perform linear regression to determine trends in dog ratings over time.
Visualization
Scatter Plot with Trend Line: Visualize ratings over time along with a linear trend line to assess rating inflation.
