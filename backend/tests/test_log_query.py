from blockchain_client import log_drug_query

def test_log_query():
    drug_to_log = "atorvastatin"  # Example drug name
    try:
        tx_hash = log_drug_query(drug_to_log)
        print(f"Successfully logged '{drug_to_log}' to blockchain.")
        print(f"Transaction Hash: {tx_hash}")
        print(f"View on Etherscan: https://sepolia.etherscan.io/tx/{tx_hash}")
    except Exception as e:
        print(f"❌ Error logging to blockchain: {e}")

if __name__ == "__main__":
    test_log_query()
