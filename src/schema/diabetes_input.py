from pydantic import BaseModel, Field

class DiabetesInput(BaseModel):
    Pregnancies: int = Field(..., ge=0)
    Glucose: float = Field(..., gt=0)
    BloodPressure: float = Field(..., gt=0)
    SkinThickness: float = Field(..., ge=0)
    Insulin: float = Field(..., ge=0)
    BMI: float = Field(..., gt=0)
    DiabetesPedigreeFunction: float = Field(..., gt=0)
    Age: int = Field(..., gt=0)