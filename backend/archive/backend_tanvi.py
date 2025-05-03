# keep in alphabetical order to keep it clean
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import APIRouter, Request, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from typing import Union, List

import os
import shutil
import uvicorn

### Custom libraries
from pinecone_query import init_resources, clear_resources, retrieve_drugs
from gemini_response import generate_medication_summary

###


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_resources()
    yield
    clear_resources()

app = FastAPI(lifespan=lifespan)
router = APIRouter()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow credentials (e.g., cookies, authorization headers)
    allow_methods=["*"],    # Specify allowed HTTP methods (or use wildcard "*")
    allow_headers=["*"],    # Specify allowed HTTP headers (or use wildcard "*")
)


# CLASSES
''' class for vector db _ query'''
class QueryRequest(BaseModel):
    query_text: str
    
''' class for gemini_response'''
class MedicationEntry(BaseModel): #workin progress
    name: str
    definition: str

class PatientProfile(BaseModel):
    age: int
    conditions: list[str] = []
    allergies: list[str] = []

class MedicationRequest(BaseModel):
    medications: list[MedicationEntry]
    profile: PatientProfile

@app.get("/")
async def api_entry():
    return {"Welcome": "RX-Check API"}

# Endpoint to handle CSV upload
@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    return {"Function": "Function"}

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

    # You can still split by commas if needed:
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
    {
      "name": "Atorvastatin",
      "definition": "Atorvastatin is used to lower cholesterol and belongs to the statin class of drugs."
    },
    {
      "name": "Lisinopril",
      "definition": "Lisinopril is used to treat high blood pressure and heart failure."
    }
  ],
  "profile": {
    "age": 65,
    "conditions": ["hypertension", "high cholesterol"],
    "allergies": ["penicillin"]
  }
}

'''
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
