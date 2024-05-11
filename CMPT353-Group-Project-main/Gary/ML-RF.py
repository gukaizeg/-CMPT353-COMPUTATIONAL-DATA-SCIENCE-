import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

data = pd.read_csv("covid_and_employment_total_included.csv")

cities = data['GEO'].unique()

results = pd.DataFrame(columns=['City', 'MSE', 'MAE', 'Feature Importance'])

for city in cities:
    
    city_data = data[data['GEO'] == city]

    features = city_data[['covid cases', 'covid deaths']]
    target = city_data['total unemployment rate(%)']

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)

    rf_model = RandomForestRegressor(n_estimators=100, min_samples_split=2, min_samples_leaf=1)

    rf_model.fit(X_train, y_train)

    predictions = rf_model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    feature_importances = rf_model.feature_importances_

    result = pd.DataFrame({'City': [city], 'MSE': [mse], 'MAE': [mae], 
                          'Feature Importance': [feature_importances]})
    results = pd.concat([results, result], ignore_index=True)

results.to_csv('RF_results.csv', index=False)

import matplotlib.pyplot as plt
import numpy as np

X = np.arange(len(cities))

plt.figure(figsize=(10, 5))

# Plotting MSE
plt.plot(X, results['MSE'], 'o-', color='blue', label='MSE')

# Plotting MAE
plt.plot(X, results['MAE'], 'o-', color='red', label='MAE')

plt.title('MSE and MAE by City')
plt.xticks(X, cities, rotation=90)
plt.ylabel('Error')
plt.legend()

plt.tight_layout()

plt.savefig('RF_results_figure.png')