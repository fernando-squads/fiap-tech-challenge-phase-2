from dotenv import load_dotenv
from fastapi import FastAPI
from src.schemas import DiabetesInput, DiabetesOutput
from src.predictor import DiabetesPredictor

load_dotenv()

app = FastAPI(
    title="Diabetes Prediction API",
    description="API para predição de diabetes usando rede neural otimizada",
    version="1.0.0"
)

predictor = DiabetesPredictor()

@app.post("/predict", response_model=DiabetesOutput)
def predict_diabetes(input_data: DiabetesInput):
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

    return {
        "prediction": prediction,
        "probability": round(probability, 4),
        "diagnosis": "Diabetes" if prediction == 1 else "Não Diabetes",
        "message": message
    }