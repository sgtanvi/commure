from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Path
from fastapi.responses import JSONResponse
from db import prescriptions_collection
from datetime import datetime, timezone
import shutil
import os

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/prescriptions/{user_id}")
async def get_active_prescriptions(user_id: str = Path(...)):
    user = await prescriptions_collection.find_one({"user_id": user_id})
    
    if not user:
        return {"user_id": user_id, "prescriptions": []}

    active_prescriptions = []

    for doc in user.get("documents", []):
        # If single-med format
        if "pres_name" in doc and doc.get("active"):
            active_prescriptions.append({
                "pres_name": doc["pres_name"],
                "pres_strength": doc.get("pres_strength"),
                "directions": doc.get("directions"),
                "date_prescribed": doc.get("date_prescribed"),
                "family_member_name": doc.get("family_member_name"),
                "num_refills": doc.get("num_refills"),
                "date_uploaded": doc.get("date_uploaded")
            })

        # If multi-med format
        if "prescriptions" in doc:
            for med in doc["prescriptions"]:
                if med.get("active"):
                    active_prescriptions.append({
                        "pres_name": med["pres_name"],
                        "pres_strength": med.get("pres_strength"),
                        "date_prescribed": doc.get("date_prescribed"),
                        "family_member_name": doc.get("family_member_name"),
                        "num_refills": doc.get("num_refills"),
                        "date_uploaded": doc.get("date_uploaded")
                    })
                    
    return {"user_id": user_id, "active_prescriptions": active_prescriptions}


@app.post("/upload/")
async def upload_prescription(user_id: str = Form(...), file: UploadFile = File(...)):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Invalid file type. Must be PDF.")
        
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        parsed_data = {
            "prescriptions": [
                {"pres_name": "TEMAZEPAM", "pres_strength": "10 mg", "active": True},
                {"pres_name": "CEFUROXIME", "pres_strength": "1.5 g", "active": True},
                {"pres_name": "METRONIDAZOLE", "pres_strength": "500 mg", "active": True},
                {"pres_name": "BRUFEN", "pres_strength": "800 mg", "active": True}
            ],
            "date_prescribed": "2025-04-04",
            "family_member_name": "Unknown",
            "num_refills": 0,
            "date_uploaded": datetime.now(timezone.utc)
        }

        await prescriptions_collection.update_one(
            {"user_id": user_id},
            {"$push": {"documents": parsed_data}},
            upsert=True
        )

        os.remove(file_path)

        return {"message": "Hardcoded prescription saved", "data": parsed_data}
    
    except Exception as e:
        print("Internal Server Error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
