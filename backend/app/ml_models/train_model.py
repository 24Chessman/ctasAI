# app/ml_models/train_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import xgboost as xgb
import pickle
import os

# Load the historical data
def load_data():
    """Loads the labeled dataset from CSV."""
    file_path = "historical_data_labeled.csv"
    df = pd.read_csv(file_path)
    return df

def prepare_data(df):
    """
    Prepares the data for training.
    - Converts dates to a numerical feature (day of year)
    - Encodes the target labels ('NORMAL', 'CYCLONE') into numbers
    - Selects feature columns
    """
    # Convert date to datetime and extract the day of the year (1-365)
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_year'] = df['date'].dt.dayofyear

    # Define features (X) and target (y)
    features = ['day_of_year', 'wind_speed', 'pressure', 'wave_height', 'water_level']
    X = df[features]
    y = df['label']  # This is our target: 'NORMAL', 'CYCLONE', 'FLOOD'

    # Encode the target labels into numbers (e.g., NORMAL->0, CYCLONE->1, FLOOD->2)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    return X, y_encoded, le, features

def train_xgboost_model(X, y):
    """Trains an XGBoost classifier and returns the model."""
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the model
    model = xgb.XGBClassifier(objective='multi:softmax', num_class=3, random_state=42)
    model.fit(X_train, y_train)

    # Check the model's accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model trained with accuracy: {accuracy:.2f}")

    return model, X_test, y_test

def save_model(model, label_encoder, features):
    """Saves the trained model and label encoder to disk for later use."""
    # Create a dictionary of everything to save
    model_package = {
        'model': model,
        'label_encoder': label_encoder,
        'features': features
    }
    with open('model.pkl', 'wb') as f:
        pickle.dump(model_package, f)
    print("Model saved as 'model.pkl'.")

# Main execution
if __name__ == "__main__":
    print("Loading and preparing data...")
    df = load_data()
    X, y_encoded, label_encoder, features = prepare_data(df)

    print("Training XGBoost model...")
    model, X_test, y_test = train_xgboost_model(X, y_encoded)

    print("Saving model...")
    save_model(model, label_encoder, features)

    print("\nTraining complete!")