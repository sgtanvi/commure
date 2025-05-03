from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec, CloudProvider, AwsRegion, VectorType
import os
from sentence_transformers import SentenceTransformer
import pandas as pd
from uuid import uuid4
from tqdm import tqdm


load_dotenv()
pinecone_api = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "medmate-interactions"
NAMESPACE = "default"
MODEL_NAME = "all-MiniLM-L6-v2"

# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api)

# Create a new serverless index if not already created
# Just connect to the existing index by name
index_description = pc.describe_index(name=INDEX_NAME)
idx = pc.Index(host=index_description.host)


# Load drug dataset
df = pd.read_csv("drugs.csv").fillna("Unknown")
model = SentenceTransformer(MODEL_NAME)

# Build and upsert embeddings
vectors = []
for _, row in df.iterrows():
    generic_name = row["generic_name"]
    drug_class = row["drug_classes"]
    alcohol = row["alcohol"]
    pregnancy = row["pregnancy_category"]
    csa = row["csa"]
    indications = row["indications"] if "indications" in row else "various medical conditions"

    # Split combo names like "ethinyl estradiol / norgestimate"
    components = [name.strip() for name in generic_name.split("/")]

    for name in components:
        text = (
            f"{name} is a medication often found in the combination drug '{generic_name}'. "
            f"It belongs to the {drug_class} class and is used to treat {indications}. "
            f"It is categorized as {row['rx_otc']}, pregnancy category {pregnancy}, "
            f"CSA schedule {csa}, and has alcohol interaction status '{alcohol}'."
        )
        embedding = model.encode(text).tolist()

        metadata = {
            "generic_name": name.lower(),
            "full_name": generic_name,
            "drug_class": drug_class,
            "alcohol": alcohol,
            "pregnancy": pregnancy,
            "csa": csa,
            "brand_names": row["brand_names"],
            "rx_otc": row["rx_otc"],
            "rating": row["rating"]
        }


        vectors.append((str(uuid4()), embedding, metadata))

# Upload in batches to avoid timeouts
batch_size = 100
for i in tqdm(range(0, len(vectors), batch_size), desc="Uploading to Pinecone"):
    batch = vectors[i:i+batch_size]
    idx.upsert(vectors=batch, namespace="default")

print("Upload complete.")
