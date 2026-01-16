from dotenv import load_dotenv
from src.monitoring import logging
from fastapi import FastAPI
from src.schema import DiabetesInput, DiabetesOutput
from src.model import DiabetesPredictor

load_dotenv()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Diabetes Prediction API",
    description="API para predição de diabetes usando rede neural otimizada",
    version="1.0.0"
)

predictor = DiabetesPredictor()

@app.post("/predict", response_model=DiabetesOutput)
def predict_diabetes(input_data: DiabetesInput):
    logger.info(f"Iniciando requisição na API /predict")
    data = [
        input_data.Pregnancies,
        input_data.Glucose,
        input_data.BloodPressure,
        input_data.SkinThickness,
        input_data.Insulin,
        input_data.BMI,
        input_data.DiabetesPedigreeFunction,
        input_data.Age,
    ]

    prediction, probability, message = predictor.predict(data)

    logger.info(f"Requisição na API /predict realizada com sucesso!")

    return {
        "prediction": prediction,
        "probability": round(probability, 4),
        "diagnosis": "Diabetes" if prediction == 1 else "Não Diabetes",
        "message": message
    }