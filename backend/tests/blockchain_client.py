# blockchain_client.py

from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to Ethereum node
web3 = Web3(Web3.HTTPProvider(os.getenv("ETH_NODE_URL")))

# Load Contract
CONTRACT_ADDRESS = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))

# Minimal ABI with logQuery function and DrugQueried event
ABI = [
    {
        "inputs": [{"internalType": "string", "name": "drug", "type": "string"}],
        "name": "logQuery",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
            {"indexed": False, "internalType": "string", "name": "drug", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "DrugQueried",
        "type": "event"
    }
]

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def log_drug_query(drug_name: str):
    private_key = os.getenv("PRIVATE_KEY")
    account = web3.eth.account.from_key(private_key)

    txn = contract.functions.logQuery(drug_name).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 200000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    return web3.to_hex(tx_hash)
