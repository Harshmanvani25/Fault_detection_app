# pipeline/halpha/model.py

import os
import joblib
from utils.resource_path import resource_path

class HAlphaModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self._load_model()

    def _load_model(self):
        """
        Load model and scaler in a way that works
        both in normal Python and in PyInstaller exe.
        """
    
        model_path = resource_path(
            os.path.join("pipeline", "halpha", "Models", "random_forest_fault_model_new.pkl")
        )
    
        scaler_path = resource_path(
            os.path.join("pipeline", "halpha", "Models", "rf_scaler_new.pkl")
        )
    
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
        except Exception as e:
            raise RuntimeError(f"Model loading failed: {e}")
    def predict(self, feature_array):
        """
        feature_array: numpy array shape (1, 4)
        """

        import pandas as pd

        feature_df = pd.DataFrame(
            feature_array,
            columns=[
                "mean_mean",
                "rms_ratio_mean",
                "ader",
                "zcr_raw"
            ]
        )
        
        scaled = self.scaler.transform(feature_df)
        prediction = self.model.predict(scaled)[0]

        return prediction# -*- coding: utf-8 -*-



