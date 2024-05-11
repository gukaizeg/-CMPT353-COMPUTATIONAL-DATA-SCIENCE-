import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def main():
    # Load labelled data
    labelled_data = pd.read_csv(sys.argv[1])

    # Preprocessing
    X = labelled_data.drop(['city', 'year'], axis=1)  # Features
    y = labelled_data['city']  # Target variable

    # Normalizing the features
    scaler = StandardScaler()
    X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    # Splitting into train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

    # Training a Random Forest model
    model = RandomForestClassifier(n_estimators=200,max_depth=10)
    model.fit(X_train, y_train)

    # Evaluating the model
    val_predictions = model.predict(X_val)
    print(f"Model Score: {accuracy_score(y_val, val_predictions)}")
    
    #df = pd.DataFrame({'truth': y_val, 'prediction': val_predictions})

    # Print out the rows where the truth doesn't match the prediction
    #print(df[df['truth'] != df['prediction']])
    

    # Predicting on the unlabelled data
    unlabelled_data = pd.read_csv(sys.argv[2])
    try:
        unlabelled_data = unlabelled_data.drop(['city'], axis=1)
    except KeyError:
        pass
    unlabelled_data = unlabelled_data.drop(['year'], axis=1)
    unlabelled_data = pd.DataFrame(scaler.transform(unlabelled_data), columns=unlabelled_data.columns)  # Apply the same scaling

    predictions = model.predict(unlabelled_data)
    pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)


if __name__ == "__main__":
    main()

