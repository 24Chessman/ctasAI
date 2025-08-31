# backend/app/api/endpoints/prediction_service.py
from app.ml_models.cyclone_predictor import cyclone_predictor
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        self.predictor = cyclone_predictor
    
    def predict_cyclone(self, data):
        """
        Predict cyclone probability from sensor data
        
        Args:
            data: Dictionary or DataFrame containing sensor readings
        
        Returns:
            Prediction result with probability and classification
        """
        try:
            # Convert to DataFrame if it's a dictionary
            if isinstance(data, dict):
                data = pd.DataFrame([data])
            
            # Get prediction from the model
            prediction = self.predictor.predict(data)
            
            # Format the response to match frontend expectations
            formatted_response = {
                "probability": prediction.get("probability", 0),
                "classification": prediction.get("classification", "UNKNOWN"),
                "confidence": prediction.get("confidence", 0),
                "all_probabilities": prediction.get("all_probabilities", {})
            }
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return {"error": str(e)}
    
    def predict_batch(self, data_list):
        """
        Predict cyclone probability for a batch of sensor data
        
        Args:
            data_list: List of dictionaries or DataFrame containing multiple sensor readings
        
        Returns:
            List of prediction results
        """
        try:
            # Convert to DataFrame if it's a list of dictionaries
            if isinstance(data_list, list) and isinstance(data_list[0], dict):
                data_list = pd.DataFrame(data_list)
            
            # Get predictions from the model
            predictions = self.predictor.predict_batch(data_list)
            
            # Format each prediction to match frontend expectations
            formatted_predictions = []
            for prediction in predictions:
                formatted_predictions.append({
                    "probability": prediction.get("probability", 0),
                    "classification": prediction.get("classification", "UNKNOWN"),
                    "confidence": prediction.get("confidence", 0),
                    "all_probabilities": prediction.get("all_probabilities", {})
                })
            
            return formatted_predictions
            
        except Exception as e:
            logger.error(f"Error in batch prediction: {e}")
            return {"error": str(e)}

# Create a singleton instance
prediction_service = PredictionService()