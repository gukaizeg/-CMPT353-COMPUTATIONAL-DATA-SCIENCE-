import os
import pandas as pd

# Function to combine CSV files in a folder
def combine_csvs_in_folder(folder_path):
    all_dataframes = []
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            all_dataframes.append(df)
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    return combined_df

# List of folder paths where CSV files are located
folders = [
    '../Resources Files/LabourForce2019',
    '../Resources Files/LabourForce2020',
    '../Resources Files/LabourForce2021',
    '../Resources Files/LabourForce2022',
    '../Resources Files/LabourForce2023',
]

# Combine CSVs from all folders
combined_dataframes = [combine_csvs_in_folder(folder_path) for folder_path in folders]

# Concatenate dataframes from all folders into a single dataframe
final_combined_df = pd.concat(combined_dataframes, ignore_index=True)

# Save the final combined dataframe to a new CSV file
final_combined_df.to_csv('../Result Files/combined.csv', index=False)