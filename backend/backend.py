from contextlib import asynccontextmanager
from datetime import datetime, timezone
from dotenv import load_dotenv
from fastapi import APIRouter, Request, FastAPI, File, Form, HTTPException, Path, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from typing import Optional, Union, List
import shutil
import os
import uvicorn

# Custom Libraries
from pinecone_query import init_resources, clear_resources, retrieve_drugs
from gemini_response import generate_medication_summary
from db import prescriptions_collection

load_dotenv()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_resources()
    yield
    clear_resources()


app = FastAPI(lifespan=lifespan)
router = APIRouter()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Models ===
class QueryRequest(BaseModel):
    query_text: str

class MedicationEntry(BaseModel):
    name: str
    definition: str

class PatientProfile(BaseModel):
    age: int
    conditions: list[str] = []
    allergies: list[str] = []

class MedicationRequest(BaseModel):
    medications: list[MedicationEntry]
    profile: PatientProfile

class Prescription(BaseModel):
    pres_name: str
    pres_strength: str
    refills: int
    date_prescribed: str
    active: bool

class PrescriptionDocument(BaseModel):
    prescriptions: List[Prescription]
    date_uploaded: datetime

class UserData(BaseModel):
    user_id: str
    family_members: Optional[List[str]] = []
    documents: List[PrescriptionDocument] = []

# === API Routes ===

@app.get("/")
async def api_entry():
    return {"Welcome": "RX-Check API"}

@app.post("/query-drug/")
async def query_drug(request: QueryRequest):
    query_text = request.query_text.strip()
    if not query_text:
        raise HTTPException(status_code=400, detail="Query is empty.")

    queries = [q.strip() for q in query_text.split(",") if q.strip()]
    results = []
    for q in queries:
        result = retrieve_drugs(q)
        results.append({"query": q, **result})

    return JSONResponse(content={"results": results})

@app.post("/generate_plan")
async def generate_medication_plan(data: MedicationRequest):
    if not data.medications:
        raise HTTPException(status_code=400, detail="Medication list is empty.")
    try:
        meds_str = "\n".join([f"- {m.name}: {m.definition}" for m in data.medications])
        profile_str = (
            f"Age: {data.profile.age}\n"
            f"Conditions: {', '.join(data.profile.conditions) or 'None'}\n"
            f"Allergies: {', '.join(data.profile.allergies) or 'None'}"
        )
        html_output = generate_medication_summary(meds_str, profile_str)
        return {"html": html_output}
    except Exception as e:
        print(f"Error generating plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/")
async def upload_prescription(user_id: str = Form(...), file: UploadFile = File(...)):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Invalid file type. Must be PDF.")

        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        prescription_data = {
            "prescriptions": [
                {"pres_name": "TEMAZEPAM", "pres_strength": "10 mg", "refills": 1, "date_prescribed": "2025-04-04", "active": True},
                {"pres_name": "CEFUROXIME", "pres_strength": "1.5 g", "refills": 2, "date_prescribed": "2025-04-04", "active": True},
                {"pres_name": "METRONIDAZOLE", "pres_strength": "500 mg", "refills": 1, "date_prescribed": "2025-04-04", "active": True},
                {"pres_name": "BRUFEN", "pres_strength": "800 mg", "refills": 0, "date_prescribed": "2025-04-04", "active": True}
            ],
            "date_uploaded": datetime.now(timezone.utc)
        }

        await prescriptions_collection.update_one(
            {"user_id": user_id},
            {
                "$setOnInsert": {"family_members": ["mom456", "dad789"]},
                "$push": {"documents": prescription_data}
            },
            upsert=True
        )

        os.remove(file_path)
        return {"message": "Hardcoded prescription saved", "data": prescription_data}

    except Exception as e:
        print("Internal Server Error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/prescriptions/{user_id}")
async def get_active_prescriptions(user_id: str = Path(...)):
    user = await prescriptions_collection.find_one({"user_id": user_id})
    if not user:
        return {"user_id": user_id, "active_prescriptions": []}

    active_prescriptions = []
    for doc in user.get("documents", []):
        for med in doc.get("prescriptions", []):
            if med.get("active"):
                active_prescriptions.append({
                    "pres_name": med.get("pres_name"),
                    "pres_strength": med.get("pres_strength"),
                    "refills": med.get("refills"),
                    "date_prescribed": med.get("date_prescribed"),
                    "date_uploaded": doc.get("date_uploaded")
                })

    return {"user_id": user_id, "active_prescriptions": active_prescriptions}

# ✅ NEW Gemini Summary Endpoint
@app.get("/summaries/{user_id}")
async def get_gemini_summary(user_id: str = Path(...)):
    user = await prescriptions_collection.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    meds = []
    for doc in user.get("documents", []):
        for med in doc.get("prescriptions", []):
            if med.get("active"):
                meds.append(f"- {med.get('pres_name')}: {med.get('pres_strength')}")

    if not meds:
        raise HTTPException(status_code=404, detail="No active prescriptions.")

    profile_str = "Age: 65\nConditions: None\nAllergies: None"
    meds_str = "\n".join(meds)

    try:
        html_output = generate_medication_summary(meds_str, profile_str)
        return {"html": html_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
