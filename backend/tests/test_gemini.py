import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
gemini_api = os.getenv("GEMINI_API_KEY")  # or paste directly as a string

# Configure
genai.configure(api_key=gemini_api)

# Create model
model = genai.GenerativeModel("gemini-1.5-pro")

# Run a test prompt
response = model.generate_content("Say hello in 3 different languages")

print(response.text)
'''awesome this works - Tanvi'''