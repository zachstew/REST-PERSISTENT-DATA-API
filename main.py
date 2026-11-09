import json
from pathlib import Path

from flask import Flask, request, jsonify, g
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from models import ClinicalData
from schemas import ClinicalDataCreate, ClinicalDataRead

app = Flask(__name__)

# ---------------------------------------------------------------
# 1. Create tables on startup
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------
# 2. JSON-Lines file helpers
DATA_FILE = Path("data/clinical_data.jsonl")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists

def append_to_file(record: dict):
    """Append a single clinical record as a JSON string followed by a newline."""
    with DATA_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

# ---------------------------------------------------------------
# 3. Session request
@app.before_request
def create_session():
    g.db = SessionLocal()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db: Session = g.pop("db", None)
    if db is not None:
        db.close()

# ---------------------------------------------------------------
# 4. POST /clinical/ - new record
@app.route("/clinical/", methods=["POST"])
def create_record():
    try:
        payload = request.get_json(force=True)
        clinical_data = ClinicalDataCreate(**payload)
    except Exception as exc:  # includes ValidationError, TypeError, etc.
        return jsonify({"detail": str(exc)}), 400

    db: Session = g.db
    db_item = ClinicalData(
        patient_name=clinical_data.patient_name,
        age=clinical_data.age,
        diagnosis=clinical_data.diagnosis,
        blood_pressure=clinical_data.blood_pressure,
        heart_rate=clinical_data.heart_rate,
        allergies=clinical_data.allergies,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # Write the same record to the JSON file
    file_record = db_item.to_dict()
    append_to_file(file_record)

    return jsonify(file_record), 201

# ---------------------------------------------------------------
# 5. GET /clinical/ - list all records
@app.route("/clinical/", methods=["GET"])
def read_records():
    db: Session = g.db
    records = db.query(ClinicalData).all()
    return jsonify([r.to_dict() for r in records])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)