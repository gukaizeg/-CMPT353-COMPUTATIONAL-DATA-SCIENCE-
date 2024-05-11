import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the station and city data files
stations_file = sys.argv[1]
city_data_file = sys.argv[2]

# Read the station data as a line-by-line JSON file
stations = pd.read_json(stations_file, lines=True)

# Read the city data from the CSV file
cities = pd.read_csv(city_data_file)

# Define a function to calculate the distance between a city and all stations
def distance(city, stations):
    lat1, lon1 = np.radians(city['latitude']), np.radians(city['longitude'])
    lat2, lon2 = np.radians(stations['latitude']), np.radians(stations['longitude'])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    distance = 6371 * c  # Radius of the Earth in km
    return distance

# Define a function to find the best 'avg_tmax' value for a city from the stations
def best_tmax(city, stations):
    city_distance = distance(city, stations)
    min_distance_idx = np.argmin(city_distance)
    return stations.iloc[min_distance_idx]['avg_tmax'] / 10

# Calculate the 'avg_tmax' values for all cities
cities['avg_tmax'] = cities.apply(best_tmax, stations=stations, axis=1)

# Remove cities with missing area or population
cities = cities.dropna(subset=['area', 'population'])

# Convert the area from m² to km²
cities['area'] = cities['area'] / 1000000

# Calculate the population density
cities['population_density'] = cities['population'] / cities['area']

# Filter out cities with area greater than 10000 km²
cities = cities[cities['area'] <= 10000]

# Create a scatterplot of average maximum temperature against population density
plt.scatter(cities['avg_tmax'], cities['population_density'], color='black', alpha=0.5, s=10)
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.ylabel('Population Density (people/km\u00b2)')
plt.title('Temperature vs Population Density')

# Save the plot to the specified output file
output_file = sys.argv[3]
plt.savefig(output_file)
plt.show()
