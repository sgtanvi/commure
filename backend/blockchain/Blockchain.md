## 🛡️ Blockchain-Powered Audit Trail

### Overview

To enhance **transparency and verifiability**, RX-Check now includes **blockchain-backed logging** for all medication lookup queries. Every query to `/query-drug/` is immutably recorded on the **Ethereum Sepolia Testnet**, providing a tamper-proof audit trail without exposing any personal data.

---

### How It Works

1. **Custom Smart Contract Deployment**

   * A lightweight Solidity contract `DrugQueryLogger` deployed on Sepolia.
   * Emits an event recording the queried drug and timestamp.

2. **Python Web3 Integration**

   * Backend uses **Web3.py** to send transactions to the smart contract.
   * Transaction hashes are returned in API responses for verification.

3. **Verifiable Audit Trail**

   * Users or auditors can view transaction records on **Sepolia Etherscan**.
   * [DEVELOPER]: Note that you can use Ethereum Sepolia Faucet from google which is currently beta.

---

### Contract Example

```solidity
event DrugQueried(address indexed user, string drug, uint256 timestamp);

function logQuery(string memory drug) public {
    emit DrugQueried(msg.sender, drug, block.timestamp);
}
```

---

### Developer Setup

#### 1. **Environment Variables**

Add the following to your `.env`:

```
ETH_NODE_URL=https://eth-sepolia.g.alchemy.com/v2/your-api-key
CONTRACT_ADDRESS=0xYourDeployedContractAddress
PRIVATE_KEY=YourTestnetWalletPrivateKey
```

#### 2. **Dependencies**

```bash
pip install web3 python-dotenv
```

#### 3. **Testing Blockchain Logging**

```bash
python backend/tests/test_log_query.py
```

#### 4. **API Usage Example**

```json
POST /query-drug/
{
  "query_text": "atorvastatin"
}
```

Example Response:

```json
{
  "tx_hash": "0x1234abcd...",
  "results": [...]
}
```

---

### How to Verify Logs

1. Visit [Sepolia Etherscan](https://sepolia.etherscan.io/).
2. Search for your **Transaction Hash** or **Contract Address**.
3. View the **DrugQueried events** for immutable record of queries.
