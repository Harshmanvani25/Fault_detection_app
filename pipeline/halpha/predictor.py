    # -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 16:34:57 2026

@author: Harsh
"""

# pipeline/halpha/predictor.py

import numpy as np
from .loader import prepare_halpha_file
from .feature_extractor import extract_features_from_excel
from .model import HAlphaModel


# =============================
# CLASS LABEL MAPPING
# =============================

CLASS_NAMES = {
    0: "NORMAL",
    1: "NOISY SIGNAL",
    2: "DC OFFSET",
    3: "SATURATION",
    4: "STUCK AT ZERO"
}


# =============================
# LOAD MODEL ONCE (Singleton)
# =============================
_model_instance = None

def get_model():
    global _model_instance
    if _model_instance is None:
        _model_instance = HAlphaModel()
    return _model_instance

def predict_halpha_file(file_path, progress_callback=None):
    """
    Full HAlpha prediction pipeline.

    Steps:
    1. Normalize Excel structure (sheet/column handling)
    2. Extract features (exact training logic)
    3. Scale + Predict
    4. Return class label string
    """

    try:
        if progress_callback:
            progress_callback(5)
    
        normalized_path = prepare_halpha_file(file_path)
    
        if progress_callback:
            progress_callback(15)
    
        features = extract_features_from_excel(
            normalized_path,
            progress_callback=progress_callback
        )
    
        if progress_callback:
            progress_callback(85)
    
        model = get_model()
        prediction = model.predict(features)
    
        if progress_callback:
            progress_callback(100)
    
        return CLASS_NAMES.get(prediction, "UNKNOWN")

    except Exception as e:
        raise RuntimeError(f"HAlpha prediction failed: {e}")

# def predict_halpha_file(file_path):
#     """
#     Full HAlpha prediction pipeline.

#     Steps:
#     1. Normalize Excel structure (sheet/column handling)
#     2. Extract features (exact training logic)
#     3. Scale + Predict
#     4. Return class label string
#     """

#     try:
#         # Step 1: Normalize file
#         normalized_path = prepare_halpha_file(file_path)

#         # Step 2: Feature extraction
#         features = extract_features_from_excel(normalized_path)

#         if not isinstance(features, np.ndarray):
#             raise ValueError("Feature extraction did not return numpy array.")

#         # Step 3: Model prediction
#         prediction = _model_instance.predict(features)
        

#         # Ensure scalar integer
#         if isinstance(prediction, (list, np.ndarray)):
#             prediction = prediction[0]
        
#         prediction = int(prediction)

        
#         # Step 4: Map class
#         return CLASS_NAMES.get(prediction, "UNKNOWN")

#     except Exception as e:
#         raise RuntimeError(f"HAlpha prediction failed: {e}")