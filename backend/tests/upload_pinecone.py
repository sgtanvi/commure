from pinecone import Pinecone, ServerlessSpec, CloudProvider, AwsRegion, VectorType
from sentence_transformers import SentenceTransformer
import pandas as pd
from uuid import uuid4

# Initialize Pinecone client
pc = Pinecone(api_key='')

# Create a new serverless index if not already created
# Just connect to the existing index by name
index_description = pc.describe_index(name="medmate-interactions")
idx = pc.Index(host=index_description.host)

# Load your index

# Load drug dataset
df = pd.read_csv("drugs.csv").fillna("Unknown")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Build and upsert embeddings
vectors = []
for _, row in df.iterrows():
    text = f"{row['generic_name']} is a {row['drug_classes']} drug. It is {row['rx_otc']}, pregnancy category {row['pregnancy_category']}, CSA {row['csa']}, alcohol interaction {row['alcohol']}."
    embedding = model.encode(text).tolist()
    metadata = {
        "generic_name": row["generic_name"],
        "drug_class": row["drug_classes"],
        "alcohol": row["alcohol"],
        "pregnancy": row["pregnancy_category"],
        "csa": row["csa"]
    }
    vectors.append((str(uuid4()), embedding, metadata))

# Upload in batches to avoid timeouts
batch_size = 100
for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i+batch_size]
    idx.upsert(vectors=batch, namespace="default")

print("✅ Upload complete.")


# Exact match function
# def get_exact_match(index, drug_name, namespace="default"):
#     response = index.query(
#         vector=[0.0]*384,  # dummy vector (not used when filtering)
#         filter={"generic_name": {"$eq": drug_name.lower()}},
#         top_k=1,
#         include_metadata=True,
#         namespace=namespace
#     )
#     return response.get("matches", [])

# # Semantic fallback
# def query_by_embedding(query_text, model, index, top_k=10, namespace="default"):
#     query_vector = model.encode(query_text).tolist()
#     response = index.query(
#         vector=query_vector,
#         top_k=top_k,
#         include_metadata=True,
#         namespace=namespace
#     )
#     return response.get("matches", [])

# # Unified retrieval
# def retrieve_drugs(query_text, model, index, top_k=10, namespace="default"):
#     exact_matches = get_exact_match(index, query_text, namespace)
#     if exact_matches:
#         print("Found exact match")
#         return format_results(exact_matches)

#     print("Using semantic search...")
#     semantic_matches = query_by_embedding(query_text, model, index, top_k, namespace)
#     return format_results(semantic_matches)

# Format the results for printing or JSON