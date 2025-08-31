# app/ml_models/rule_engine.py

import pandas as pd
import numpy as np

class RuleEngine:
    """
    A simple rule-based engine for initial threat detection.
    Easy to understand, explain, and verify. Used as a first pass filter.
    """

    @staticmethod
    def analyze_data_point(wind_speed, pressure, wave_height, water_level):
        """
        Analyzes a single data point against predefined rules.
        Returns a dictionary with the threat level and type.
        """
        threat_level = "LOW"
        threat_type = "NORMAL"

        # Rule 1: Cyclone Conditions (High wind, Low pressure)
        if wind_speed > 60 and pressure < 1000:
            threat_level = "EXTREME"
            threat_type = "CYCLONE"
            return {"threat_level": threat_level, "threat_type": threat_type}

        # Rule 2: Storm Surge/Flood Conditions (High water level and waves)
        if water_level > 2.0 and wave_height > 3.0:
            threat_level = "HIGH"
            threat_type = "FLOOD"
            return {"threat_level": threat_level, "threat_type": threat_type}

        # Rule 3: Potential Developing Storm
        if wind_speed > 40 and pressure < 1005:
            threat_level = "MEDIUM"
            threat_type = "STORM"
            return {"threat_level": threat_level, "threat_type": threat_type}

        # If no rules are triggered, conditions are normal.
        return {"threat_level": threat_level, "threat_type": threat_type}

# Example usage for testing:
if __name__ == "__main__":
    # Test with some example data
    test_data = {
        'wind_speed': [65, 20, 45, 10],
        'pressure': [990, 1015, 1003, 1012],
        'wave_height': [5.0, 1.0, 2.5, 0.5],
        'water_level': [3.0, 0.5, 1.0, 0.2]
    }
    test_df = pd.DataFrame(test_data)

    print("Testing Rule-Based Engine:")
    print("==========================")
    for index, row in test_df.iterrows():
        result = RuleEngine.analyze_data_point(row['wind_speed'], row['pressure'], row['wave_height'], row['water_level'])
        print(f"Data Point {index}: {result}")