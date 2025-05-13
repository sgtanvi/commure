import google.generativeai as genai
import pandas as pd
import os
from pinecone import Pinecone, ServerlessSpec, CloudProvider, AwsRegion, VectorType
from dotenv import load_dotenv
from uuid import uuid4
from tqdm import tqdm
'''
Input: 
Medications JSON File
Bool: Active
Var: Name
Var: Strength
Var: 
'''



load_dotenv()
gemini_api = os.getenv("GEMINI_API_KEY")
pinecone_api = os.getenv("PINE_CONE")
pinecone_region = os.getenv("PINECONE_ENVO")


""" print("API Key:", api_key)"""


# Configure Gemini API
genai.configure(api_key=gemini_api)


embedding_model = genai.get_model("models/embedding-001")  # Text Embedding 004

# Initialize Pinecone
pinecone.init(api_key=pinecone_api, environment=pinecone_region)
index_name = "med-gemini"

# Check embedding dimension from Gemini (can be inferred from one call)
sample_embedding = embedding_model.embed_content(
    content="acetaminophen is a pain reliever and fever reducer.",
    task_type="RETRIEVAL_DOCUMENT"
)["embedding"]
dimension = len(sample_embedding)

# Create Pinecone index if it doesn't exist
if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        index_name,
        dimension=dimension,
        metric="cosine"
    )
index = pinecone.Index(index_name)

# Load dataset
df = pd.read_csv("drug_data.csv").fillna("Unknown")

# Helper: convert row to a descriptive sentence
def row_to_text(row):
    return (
        f"{row['generic_name']} is a {row['drug_classes']} drug. "
        f"It is classified as {row['rx_otc']}, has a pregnancy category of {row['pregnancy_category']}, "
        f"a CSA schedule of {row['csa']}, and an alcohol interaction flag of {row['alcohol']}."
    )

# Embed and upload vectors
batch = []
batch_size = 100

for i, row in tqdm(df.iterrows(), total=len(df)):
    text = row_to_text(row)
    try:
        embedding = embedding_model.embed_content(content=text, task_type="RETRIEVAL_DOCUMENT")["embedding"]
        metadata = {
            "generic_name": row["generic_name"],
            "drug_class": row["drug_classes"],
            "alcohol": row["alcohol"],
            "pregnancy": row["pregnancy_category"],
            "csa": row["csa"]
        }
        batch.append((str(uuid4()), embedding, metadata))
    except Exception as e:
        print(f"Skipping row {i}: {e}")
        continue

    if len(batch) >= batch_size:
        index.upsert(batch)
        batch = []

# Final batch
if batch:
    index.upsert(batch)
