from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

SYSTEM_PROMPT = """
You are a clinical pharmacist assisting in post-prescription care. 
Your goal is to identify any potential medication conflicts and clearly explain risks, safe usage, and reminders to the patient in plain English.

Your response must use ONLY the following HTML tags:
- Headings: <h1>, <h2>, <h3>
- Paragraphs: <p>
- Lists: <ul>, <ol>, <li>
- Formatting: <strong>, <em>
Escape all double quotes (\"). Use \\n for line breaks.

Instructions:
1. Identify potential interactions using the provided medication names and descriptions.
2. Summarize what each medication does.
3. Explain any known or likely conflicts (e.g., duplicate mechanisms, metabolism issues, kidney risks).
4. Provide a safe medication schedule, including morning/evening timing and food instructions.
5. Include reminders for hydration, avoiding alcohol/caffeine, and contacting a provider in case of severe symptoms.

Do NOT introduce medications not listed. This is post-prescription support, not diagnosis or prescription.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=SYSTEM_PROMPT
)

def generate_medication_summary(medication_descriptions: str, profile: str) -> str:
    chat = model.start_chat()
    response = chat.send_message(f"""
Medications and Definitions:
{medication_descriptions}

Patient Profile:
{profile}

Please format your output using the structure described above.
""")
    return response.text


'''TEST passed'''
# if __name__ == "__main__":
#     sample_meds = """
# - Lisinopril: Lisinopril is an ACE inhibitor used to treat high blood pressure and heart failure. It can help prevent strokes, heart attacks, and kidney problems.
# - Ibuprofen: Ibuprofen is a nonsteroidal anti-inflammatory drug (NSAID) used for pain relief, fever reduction, and inflammation control.
# """

#     sample_profile = """
# Age: 65
# Conditions: hypertension, osteoarthritis
# Allergies: penicillin
# """

#     output = generate_medication_summary(sample_meds, sample_profile)
#     print(output)
