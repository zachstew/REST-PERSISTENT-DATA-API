import datetime
from pydantic import BaseModel, Field

class ClinicalDataCreate(BaseModel):
    patient_name: str = Field(..., min_length=1, examples=["John Doe"])
    age: int = Field(..., ge=0, le=120, examples=[45])
    diagnosis: str = Field(..., min_length=1, examples=["Hypertension"])

    # --- 3 new fields ---
    # Blood pressure as "systolic/diastolic", e.g. 120/80
    blood_pressure: str = Field(..., pattern=r"^\d{2,3}/\d{2,3}$", examples=["120/80"])
    heart_rate: int = Field(..., ge=20, le=250, examples=[72])
    allergies: str = Field("None reported", examples=["Penicillin"])

# The read schema includes the auto-generated fields
class ClinicalDataRead(ClinicalDataCreate):
    id: int
    recorded_at: datetime.datetime