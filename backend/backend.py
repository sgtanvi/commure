from typing import Optional, Union, List
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from dotenv import load_dotenv
from fastapi import APIRouter, Request, FastAPI, File, Form, HTTPException, Path, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import shutil
import os
import uvicorn

##### Custom Libraries
from pinecone_query import init_resources, clear_resources, retrieve_drugs, get_medication_definitions_for_gemini
from gemini_response import generate_medication_summary
from db import prescriptions_collection, users_collection

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
    definition: Optional[str] = None

class PatientProfile(BaseModel):
    firstName: str
    lastName: str
    email: str
    #README: we know this is very unsafe and should never be done in production. doing this for now for simplicity.
    password: str
    age: int
    conditions: list[str] = []
    allergies: list[str] = []
    prescriptions: list[str] = []

class MedicationRequest(BaseModel):
    medications: list[MedicationEntry]
    #README: maybe try to get rid of this. should probably be a _id reference to the patient profile.
    profile: PatientProfile

class Prescription(BaseModel):
    pres_name: str
    pres_strength: str
    refills: int
    date_prescribed: str
    active: bool

class PrescriptionDocument(BaseModel):
    user_id: str
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

## RESTRICTION: Frontend/client	Calls /query-drug/ repeatedly, stores list so implementation responsibility is on client##
'''
input: 
{
    "query_text": "ethinyl estradiol"
}

Output:
2 modes: semantic or exact
{
    "results": [
    {
        "query": "ethinyl estradiol",
        "mode": "semantic",
        "results": [
        {
            "score": 0.718, <---- Note. In exact, you wont get a score.
            "generic_name": "ethinyl estradiol and norgestimate (oral route)",
            "drug_class": "Contraceptives",
            "alcohol": "X",
            "pregnancy": "X",
            "csa": "N"
        },
        
        ...
    }]

'''

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


##### GEMINI ######

'''
input example
{
  "medications": [
    { "name": "Lisinopril" },
    { "name": "Ibuprofen" }
  ],
  "profile": {
    "age": 65,
    "conditions": ["hypertension", "osteoarthritis"],
    "allergies": ["penicillin"]
  }
}

'''
@app.post("/generate_plan")
async def generate_medication_plan(data: MedicationRequest):
    if not data.medications:
        raise HTTPException(status_code=400, detail="Medication list is empty.")
    try:
        med_names = [m.name for m in data.medications]
        pinecone_defs = get_medication_definitions_for_gemini(med_names)
        meds_str = "\n".join([f"- {m['name']}: {m['definition']}" for m in pinecone_defs])
        profile_str = (
            f"Age: {data.profile.age}\n"
            f"Conditions: {', '.join(data.profile.conditions) or 'None'}\n"
            f"Allergies: {', '.join(data.profile.allergies) or 'None'}"
        )
        html_output = generate_medication_summary(meds_str, profile_str)
        return {"html": html_output}
    except Exception as e:
        print(f"Error gen-erating plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))



class Prescription(BaseModel):
    pres_name: str
    pres_strength: str
    refills: int
    date_prescribed: str
    active: bool

class PrescriptionDocument(BaseModel):
    user_id: str
    prescriptions: List[Prescription]
    date_uploaded: datetime

class UserData(BaseModel):
    user_id: str | None = None
    first_name: str
    last_name: str
    email: str
    password: str
    conditions: List[str] = []
    allergies: List[str] = []
    family_members: Optional[List[str]] = []
    #_id of the prescription document
    documents: str | None = None

"""
user sign up
    first_name
    last_name
    email
    password

user conditions/allergies
    conditions/alergies

user upload prescription

    documents

    class Prescription(BaseModel):
    pres_name: str
    pres_strength: str
    refills: int
    date_prescribed: str
    active: bool

    class PrescriptionDocument(BaseModel):
        prescriptions: List[Prescription]
        date_uploaded: datetime
"""

@app.post("/signup/")
async def signup(user: UserData):
    # Convert Pydantic model to dict for MongoDB storage
    user_dict = user.model_dump()
    # Insert the user into the database
    result = await users_collection.insert_one(user_dict)
    # Get the inserted _id and add it to the user dict
    user_dict["_id"] = str(result.inserted_id)
    # Return both a success message and the user data
    return {"message": "User created successfully", "user": user_dict}

@app.post("/conditions/")
async def conditions(user_id: str = Form(...), conditions: list[str] = Form(...)):
    await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"conditions": conditions}}
    )
    user = await users_collection.find_one({"_id": user_id})
    return {"message": "Conditions updated successfully", "user": user}

@app.post("/allergies/")
async def allergies(user_id: str = Form(...), allergies: list[str] = Form(...)):
    await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"allergies": allergies}}
    )
    user = await users_collection.find_one({"_id": user_id})
    return {"message": "Allergies updated successfully", "user": user}

# === Models ===
class QueryRequest(BaseModel):
    query_text: str

class MedicationEntry(BaseModel):
    name: str
    definition: Optional[str] = None

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


##### GEMINI ######

'''
input example
{
  "medications": [
    { "name": "Lisinopril" },
    { "name": "Ibuprofen" }
  ],
  "profile": {
    "age": 65,
    "conditions": ["hypertension", "osteoarthritis"],
    "allergies": ["penicillin"]
  }
}

'''
@app.post("/generate_plan")
async def generate_medication_plan(data: MedicationRequest):
    if not data.medications:
        raise HTTPException(status_code=400, detail="Medication list is empty.")
    try:
        med_names = [m.name for m in data.medications]
        pinecone_defs = get_medication_definitions_for_gemini(med_names)
        meds_str = "\n".join([f"- {m['name']}: {m['definition']}" for m in pinecone_defs])
        profile_str = (
            f"Age: {data.profile.age}\n"
            f"Conditions: {', '.join(data.profile.conditions) or 'None'}\n"
            f"Allergies: {', '.join(data.profile.allergies) or 'None'}"
        )
        html_output = generate_medication_summary(meds_str, profile_str)
        return {"html": html_output}
    except Exception as e:
        print(f"Error gen-erating plan: {e}")
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
            "user_id": user_id,
            "prescriptions": [
                {"name": "TEMAZEPAM", "pres_strength": "10 mg", "refills": 1, "date_prescribed": "2025-04-04", "active": True},
                {"name": "CEFUROXIME", "pres_strength": "1.5 g", "refills": 2, "date_prescribed": "2025-04-04", "active": True},
                {"name": "METRONIDAZOLE", "pres_strength": "500 mg", "refills": 1, "date_prescribed": "2025-04-04", "active": True},
                {"name": "BRUFEN", "pres_strength": "800 mg", "refills": 0, "date_prescribed": "2025-04-04", "active": True}
            ],
            "date_uploaded": datetime.now(timezone.utc)
        }

        prescription_coll_exists = await prescriptions_collection.find_one({"user_id": user_id})
        if prescription_coll_exists:
            result = await prescriptions_collection.update_one(
                {"user_id": user_id},
                {
                    "$setOnInsert": {"family_members": ["mom456", "dad789"]},
                    "$push": {"documents": prescription_data}
                },
                upsert=True
            )
            return {"message": "Prescription saved successfully", "data": prescription_data}
        else:
            result = await prescriptions_collection.insert_one(prescription_data)
            await users_collection.update_one(
                {"_id": user_id},
                {"$set": {"documents": str(result.inserted_id)}}
            )
            return {"message": "Prescription created successfully", "data": prescription_data}
    
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

@app.get("/summaries/{user_id}")
async def get_gemini_summary(user_id: str = Path(...)):
    user = await prescriptions_collection.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    meds = []
    for doc in user.get("documents", []):
        for med in doc.get("prescriptions", []):
            if med.get("active"):
                meds.append(f"- {med.get('name')}: {med.get('pres_strength')}")

    if not meds:
        raise HTTPException(status_code=404, detail="No active prescriptions.")

    profile_str = "Age: 65\nConditions: None\nAllergies: None"
    meds_str = "\n".join(meds)

    try:
        html_output = generate_medication_summary(meds_str, profile_str)
        return {"html": html_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    try:
        HOST = os.getenv("HOST")
        PORT = int(os.getenv("PORT"))
    except Exception:
        print(
            "Error: Please make sure you have set the HOST and PORT environment variables correctly."
        )
        exit(2)
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info",
    )


if __name__ == "__main__":
    main()
