import tensorflow as tf
import joblib
import numpy as np
from src.config import FEATURES
from src.llm_explainer import explain_with_llm

MODEL_PATH = "models/diabetes_model.keras"
SCALER_PATH = "models/scaler.pkl"

class DiabetesPredictor:
    def __init__(self):
        self.model = tf.keras.models.load_model(MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)

    def predict(self, data: list):
        X = np.array([data])
        X_scaled = self.scaler.transform(X)

        predict = self.model.predict(X_scaled)

        prob = float(predict[0][0])
        pred = int(prob > 0.5)
        message = explain_with_llm(FEATURES, data)

        return pred, prob, message