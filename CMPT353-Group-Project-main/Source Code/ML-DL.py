import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

data = pd.read_csv("covid_and_employment_total_included.csv")  

cities = data['GEO'].unique()

results = []

for city in cities:
    city_data = data[data['GEO'] == city]
    
    features = city_data[['covid cases', 'covid deaths']]
    target = city_data['total unemployment rate(%)']


    scaler = StandardScaler()
    features = scaler.fit_transform(features)


    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)


    model = Sequential()
    model.add(Dense(16, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1))

    model.compile(optimizer=Adam(), loss='mean_squared_error', metrics=['mean_absolute_error'])

    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=10, verbose=0)

    mse, mae = model.evaluate(X_test, y_test, verbose=0)

    print(f"City: {city}")
    print(f"Mean Squared Error: {mse}")
    print(f"Mean Absolute Error: {mae}")

    results.append({'City': city, 'MSE': mse, 'MAE': mae})


results_df = pd.DataFrame(results)
results_df.to_csv('DL_results.csv', index=False)
