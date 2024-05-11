## Exercise 1 - Getting Started with NumPy and Pandas

### Overview

This exercise is designed to familiarize you with the NumPy and Pandas libraries, emphasizing array manipulations and data frame operations without traditional looping constructs. The main tasks involve data processing and analysis using provided datasets.

#### Python Libraries
Ensure you have the necessary Python libraries installed:
- NumPy
- Pandas
- Statsmodels
- Jupyter

#### Tasks
1. **Data Visualization and Signal Processing:**
   - Create a sine wave signal array, simulate noisy sensor data, and attempt to filter out the noise.
   - Visualize both the original and noisy signals in a Jupyter Notebook named `signal-plot.ipynb`.

2. **Data Analysis with NumPy:**
   - Load data from `monthdata.npz` which includes precipitation data for various Canadian cities.
   - Perform analysis to determine city with the lowest total precipitation, average monthly precipitation, and more.
   - Develop a Python script `np_summary.py` to calculate and display these statistics.

#### Getting Started with Pandas
- Repeat the analysis using Pandas for enhanced data handling and output formatting, excluding quarterly totals.
- Develop a Python script `pd_summary.py` that mirrors the NumPy analysis but uses Pandas for data manipulation.

### Additional Information
Refer to the provided screenshots and instructions in the course materials to replicate the analysis and results.

## Analysis with Pandas

### Overview
Further explore data manipulation and aggregation techniques in Pandas to process and analyze a refined dataset derived from the Global Historical Climatology Network for the year 2016.

#### Task
- Implement the `monthly_totals.py` script to regenerate initial data files using Pandas, ensuring to follow the structure provided in `monthly_totals_hint.py`.

## Timing Comparison

### Overview
Compare the performance of different data pivoting methods in Pandas against a baseline implementation using loops.

#### Instructions
- Use the `timing.ipynb` notebook to run benchmarks on the provided pivoting functions.
- Ensure correctness and evaluate performance differences.

## Questions and Reflections

### Overview
Reflect on the exercises and document your experiences and findings.

#### Tasks
- Answer the provided questions in `answers.txt`, focusing on your experiences with NumPy vs Pandas and the performance analysis of pivoting functions.

