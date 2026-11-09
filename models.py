import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

class ClinicalData(Base):
    __tablename__ = "clinical_data"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    diagnosis = Column(String, nullable=False)

    # --- 3 new columns ---
    blood_pressure = Column(String, nullable=False)   # e.g. "120/80"
    heart_rate = Column(Integer, nullable=False)      # beats per minute
    allergies = Column(String, nullable=False, default="None reported")

    recorded_at = Column(DateTime, default=utc_now)

    def to_dict(self):
        """Return a JSON-serialisable dict representation."""
        return {
            "id": self.id,
            "patient_name": self.patient_name,
            "age": self.age,
            "diagnosis": self.diagnosis,
            "blood_pressure": self.blood_pressure,
            "heart_rate": self.heart_rate,
            "allergies": self.allergies,
            "recorded_at": self.recorded_at.isoformat(),
        }