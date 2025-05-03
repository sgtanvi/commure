import os
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "medmate-interactions"
NAMESPACE = "default"
MODEL_NAME = "all-MiniLM-L6-v2"

shared_state = {}

def init_resources():

    # Load embedding model once
    model = SentenceTransformer(MODEL_NAME)

    # Connect to Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_info = pc.describe_index(name=INDEX_NAME)
    index = pc.Index(host=index_info.host)
    
    shared_state["model"] = model
    shared_state["index"] = index
    
def clear_resources():
    shared_state.clear()

def retrieve_drugs(query_text:str, top_k:int = 10):
    model = shared_state["model"]
    index = shared_state["index"]
    namespace = "default" #trying to make it faster with local variable#
    
    #exact match first
    exact = index.query(
        vector=[0.0] * 384, #384 is the vector size
        filter={"generic_name": {"$eq": query_text.lower()}}, 
        top_k=1,
        include_metadata=True,
        namespace=namespace
    ).get("matches", [])
    
    if len(exact) > 0:
        return {"mode": "exact", "results": format_results(exact)}
    
    # Semantic fallback
    embedding = model.encode(query_text.lower()).tolist()
    semantic = index.query(
        vector = embedding, 
        top_k = 10,
        include_metadata = True,
        namespace = namespace
    ).get("matches", [])
    
    return {"mode": "semantic", "results": format_results(semantic)}

def get_medication_definitions_for_gemini(med_names: list[str], top_k: int = 1):
    model = shared_state["model"]
    index = shared_state["index"]
    namespace = "default"

    meds_with_defs = []

    for name in med_names:
        # Semantic search
        embedding = model.encode(name.lower()).tolist()
        res = index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
            namespace=namespace
        )

        if res.get("matches"):
            metadata = res["matches"][0]["metadata"]
            generic_name = metadata.get("generic_name", name)
            brand_names = metadata.get("brand_names", "")
            drug_class = metadata.get("drug_class", "Unknown class")
            pregnancy = metadata.get("pregnancy", "N")
            csa = metadata.get("csa", "U")
            alcohol = metadata.get("alcohol", "")
            rx_otc = metadata.get("rx_otc", "Unknown")
            rating = metadata.get("rating", "Not rated")

            # Pregnancy description
            pregnancy_risk = {
                "A": "No risk in first trimester.",
                "B": "No human risk, animal studies show none.",
                "C": "Animal risk shown; use only if benefits outweigh risks.",
                "D": "Positive evidence of fetal risk; benefits may still justify use.",
                "X": "High risk of fetal abnormalities; should not be used.",
                "N": "Not classified."
            }.get(pregnancy, "Unknown risk")

            # CSA description
            csa_class = {
                "1": "Schedule I – High abuse risk, no accepted medical use.",
                "2": "Schedule II – High abuse risk, but accepted medical use.",
                "3": "Schedule III – Moderate abuse risk, accepted use.",
                "4": "Schedule IV – Lower abuse risk.",
                "5": "Schedule V – Lowest abuse risk.",
                "N": "Not a controlled substance.",
                "M": "Multiple schedules apply.",
                "U": "Unknown CSA schedule."
            }.get(csa, "Unlisted.")

            description = f"""{generic_name} belongs to the drug class {drug_class}. 
It is available under the following brand names: {brand_names}. 
This medication is classified as {rx_otc}, with a user-reported effectiveness rating of {rating}/10. 
Pregnancy category: {pregnancy} — {pregnancy_risk} 
CSA Schedule: {csa} — {csa_class} 
Alcohol Interaction Warning: {alcohol}"""

        else:
            description = "No definition available."

        meds_with_defs.append({
            "name": name,
            "definition": description.strip()
        })

    return meds_with_defs


def format_results(matches):
    return [
        {
            "score": round(match["score"], 3),
            "generic_name": match["metadata"]["generic_name"],
            "drug_class": match["metadata"]["drug_class"],
            "alcohol": match["metadata"]["alcohol"],
            "pregnancy": match["metadata"]["pregnancy"],
            "csa": match["metadata"]["csa"]
        }
        for match in matches
    ]

# # Test entry point
# if __name__ == "__main__":
#     results = retrieve_drugs("atorvastatin", model, index)
#     for r in results:
#         print(r)
