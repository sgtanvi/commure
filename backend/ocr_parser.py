from pdf2image import convert_from_path
import pytesseract
import re


from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(file_path: str, page_limit: int = -1) -> str:
    # Try extracting with PyPDF (for text-based PDFs)
    try:
        reader = PdfReader(file_path)
        pages = reader.pages[:page_limit] if page_limit > 0 else reader.pages
        text = "\n".join(page.extract_text() or "" for page in pages)

        if text.strip():  # If there's any readable text, use it
            return text
    except Exception as e:
        print(f"[PyPDF] Error extracting text: {e}")

    # Fallback to OCR
    try:
        images = convert_from_path(file_path)
        if page_limit > 0:
            images = images[:page_limit]
        text = "\n".join(pytesseract.image_to_string(img) for img in images)
        return text
    except Exception as e:
        print(f"[OCR] Error extracting text via OCR: {e}")
        return ""


import re
from typing import List

def parse_prescription(text: str) -> dict:
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    ignore_keywords = [
        "Prophylactic", "Route Given", "Patient identification", "Dose Route", "instructions",
        "Date of admission", "Date of planned discharge", "Chart Number", "Consultant", "DOB", "Ward",
        "This prescription sheet", "Terms and Conditions", "Downloaded from"
    ]
    cleaned_lines = [line for line in lines if not any(k.lower() in line.lower() for k in ignore_keywords)]

    prescriptions = []

    for line in cleaned_lines:
        tokens = line.split()
        if len(tokens) >= 3:
            # Check if second token looks like a dosage (e.g., 10 mg, 1.5 g)
            dose_match = re.match(r"^\d+(\.\d+)?(mg|g|ml|mcg)$", tokens[1] + tokens[2] if len(tokens) > 2 else tokens[1], re.IGNORECASE)
            if dose_match:
                name = tokens[0]
                strength = tokens[1] + " " + tokens[2]
                prescriptions.append({
                    "pres_name": name,
                    "pres_strength": strength,
                    "active": True
                })

    return {
        "prescriptions": prescriptions,
        "date_prescribed": "2025-04-04",
        "family_member_name": "Unknown",
        "num_refills": 0
    }

