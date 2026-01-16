from pydantic import BaseModel

class DiabetesOutput(BaseModel):
    prediction: int
    probability: float
    diagnosis: str
    message: str