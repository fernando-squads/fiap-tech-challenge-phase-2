from src.monitoring import logging
import tensorflow as tf
import joblib
import pandas as pd
import numpy as np
from src.config import FEATURES, FEATURES_DF
from src.llm import explain_with_llm

MODEL_PATH = "models/diabetes_model.keras"
SCALER_PATH = "models/scaler.pkl"

class DiabetesPredictor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model = tf.keras.models.load_model(MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)


    def predict(self, input_data: list):
        self.logger.info(f"Iniciando predição utilizando os parametros: {input_data}")
        
        input_df = pd.DataFrame([input_data], columns=FEATURES_DF)
        input_scaled = self.scaler.transform(input_df)
        prediction = self.model.predict(input_scaled)

        prob = float(prediction[0][0])
        pred = int(prob > 0.5)
        message = explain_with_llm(FEATURES, input_data, prob)

        self.logger.info(f"A predição retornou a probabilidade do paciente possuir dibates de {prob}")

        return pred, prob, message