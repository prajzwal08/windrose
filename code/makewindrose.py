"""
Title: Windrose Plotting Script
Author: [Prajwal Khanal]
Date: [Monday, 29 April 2024 @ 03:04 PM]
Purpose: Generate windrose plots for individual months and seasons from wind data.

Description:
This script reads wind data from a CSV file, filters it for a specific date range, and generates windrose plots
for individual months and seasons. The windrose plots are saved as PNG image files.

Required Libraries:
- pandas
- matplotlib.pyplot
- windrose (from windrose import WindroseAxes)
- numpy
- os

Usage:
1. Ensure the CSV file containing wind data is available at the specified file path.
2. Set the output directory path where the generated windrose plots will be saved.
3. Run the script.

"""

# Required Libraries
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import numpy as np
import os

# File Paths
file_path = "/home/khanalp/data/field_data/glanerbeek/glanerbeek_wind/Field1.csv"
output_path = "/home/khanalp/code/PhD/windrose/plot/field1"

# Read CSV file into DataFrame
dframe_wind = pd.read_csv(file_path)

# Drop rows with NaN values
dframe_wind_noNA = dframe_wind.dropna()

# Convert 'Timestamps' column to pandas DateTime format
dframe_wind_noNA['Timestamps'] = pd.to_datetime(dframe_wind_noNA['Timestamps'])

# Filter DataFrame for the desired date range
df_filtered = dframe_wind_noNA.loc[(dframe_wind_noNA['Timestamps'] >= '2023-05-19') & (dframe_wind_noNA['Timestamps'] <= '2024-04-28')]

# Reset index
df_filtered.reset_index(drop=True, inplace=True)

# Define a dictionary to map month numbers to their names
month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
               7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

# Generate windrose plots for individual months
for i in range(1, 3):  # Loop over two months (for demonstration)
    # Filter DataFrame for a particular month
    selected_month = df_filtered[df_filtered['Timestamps'].dt.month == i]  
    ax = WindroseAxes.from_ax()
    ax.bar(selected_month['degrees_Wind_Direction'].values, selected_month['m/s_Wind_Speed'].values, normed=True, opening=0.8, edgecolor='white',
           bins=np.arange(0, 8, 2))
    ax.set_title(f"Windrose for {month_names[i]}, Field 1 (Glanerbeek)")  # Use month name from the dictionary
    
    # Add a note indicating wind speeds are in m/s
    ax.text(0.5, -0.1, 'Wind speeds are in m/s', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=10)
   
    # Move the legend down by adjusting the bbox_to_anchor parameter
    ax.legend(bbox_to_anchor=(-0.1, -0.1), loc='lower left')
   
    # Save the plot as an image file
    output_file = os.path.join(output_path, f"{month_names[i]}.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')  # Adjust dpi for better quality and bbox_inches for tight layout
    plt.close()  # Close the plot to free up memory

# Define a dictionary to map season names to their corresponding months
seasons = {'DJF': [12, 1, 2], 'MAM': [3, 4, 5], 'JJA': [6, 7, 8], 'SON': [9, 10, 11]}

# Generate windrose plots for seasons
for season, months in seasons.items():
    # Filter DataFrame for the current season
    selected_season = df_filtered[df_filtered['Timestamps'].dt.month.isin(months)]  
    ax = WindroseAxes.from_ax()
    ax.bar(selected_season['degrees_Wind_Direction'].values, selected_season['m/s_Wind_Speed'].values, normed=True, opening=0.8, 
           edgecolor='white', bins=np.arange(0, 8, 2))
    ax.set_title(f"Windrose Field 1 for {season}")
    
    # Add a note indicating wind speeds are in m/s
    ax.text(0.5, -0.1, 'Wind speeds are in m/s', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=10)

    # Move the legend to the left bottom corner
    ax.legend(bbox_to_anchor=(-0.1, -0.1), loc='lower left')
    
    # Save the plot as an image file
    output_file = os.path.join(output_path, f"{season}.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')  # Adjust dpi for better quality and bbox_inches for tight layout
    plt.close()  # Close the plot to free up memory

