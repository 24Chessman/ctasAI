# backend/app/ml_models/cyclone_predictor.py
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class CyclonePredictor:
    def __init__(self):
        """
        Initialize the cyclone predictor with the pre-trained XGBoost model
        """
        try:
            # Get the current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Create absolute path to model
            model_path = os.path.join(current_dir, 'model.pkl')
            
            # Check if model exists
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            # Load the model package
            model_package = joblib.load(model_path)
            self.model = model_package['model']
            self.label_encoder = model_package['label_encoder']
            self.features = model_package['features']
            
            print("XGBoost cyclone predictor initialized successfully")
            print(f"Model features: {self.features}")
            print(f"Model classes: {self.label_encoder.classes_}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            # Create a mock predictor for development
            self.model = None
            self.label_encoder = None
            self.features = ['day_of_year', 'wind_speed', 'pressure', 'wave_height', 'water_level']
            print("Warning: Using mock predictor - predictions will be random")
    
    def preprocess_data(self, new_data):
        """
        Preprocess new data to match the training data format
        """
        # Create a copy of the data
        processed_data = new_data.copy()
        
        # Convert date to day_of_year if date is provided
        if 'date' in processed_data.columns and 'day_of_year' not in processed_data.columns:
            processed_data['date'] = pd.to_datetime(processed_data['date'])
            processed_data['day_of_year'] = processed_data['date'].dt.dayofyear
        
        # Ensure we have all the required features
        for feature in self.features:
            if feature not in processed_data.columns:
                if feature == 'day_of_year':
                    # If day_of_year is missing, use current day of year
                    processed_data[feature] = datetime.now().timetuple().tm_yday
                else:
                    # For other missing features, use a default value
                    processed_data[feature] = 0
                    print(f"Warning: Missing feature {feature}, using default value 0")
        
        # Extract only the feature columns in the correct order
        X_new = processed_data[self.features]
        
        return X_new
    
    def predict(self, input_data):
        """
        Make a prediction on new data
        Handles both direct input and wrapped input (with 'data' field)
        """
        # Handle wrapped input format (with 'data' field)
        if isinstance(input_data, dict) and 'data' in input_data:
            input_data = input_data['data']
        
        # Convert to DataFrame if it's a single dictionary
        if isinstance(input_data, dict):
            new_data = pd.DataFrame([input_data])
        else:
            new_data = pd.DataFrame(input_data)
        
        if self.model is None:
            # Return mock predictions for development
            import random
            probability = random.random()
            classification = "CYCLONE" if probability > 0.5 else "NORMAL"
            return {
                "probability": float(probability),
                "classification": classification,
                "confidence": abs(probability - 0.5) * 2
            }
        
        try:
            # Preprocess the data
            X_processed = self.preprocess_data(new_data)
            
            # Make prediction
            prediction = self.model.predict(X_processed)
            probabilities = self.model.predict_proba(X_processed)
            
            # Convert prediction to label
            predicted_label = self.label_encoder.inverse_transform(prediction)[0]
            
            # Get probability for the predicted class
            probability = probabilities[0][prediction[0]]
            
            # For binary classification, we might want to focus on CYCLONE probability
            if "CYCLONE" in self.label_encoder.classes_:
                cyclone_idx = list(self.label_encoder.classes_).index("CYCLONE")
                cyclone_probability = probabilities[0][cyclone_idx]
                
                return {
                    "probability": float(cyclone_probability),
                    "classification": predicted_label,
                    "confidence": abs(cyclone_probability - 0.5) * 2,
                    "all_probabilities": {cls: float(prob) for cls, prob in zip(self.label_encoder.classes_, probabilities[0])}
                }
            else:
                return {
                    "probability": float(probability),
                    "classification": predicted_label,
                    "confidence": abs(probability - 0.5) * 2,
                    "all_probabilities": {cls: float(prob) for cls, prob in zip(self.label_encoder.classes_, probabilities[0])}
                }
            
        except Exception as e:
            return {"error": str(e)}
    

# Create a singleton instance
cyclone_predictor = CyclonePredictor()