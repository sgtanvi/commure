# RX-Check

AI-powered medication clarity and safety platform.

Built during the Commure Hackathon 2025, RX-Check helps patients and caregivers manage medications post-discharge by combining LLMs and vector search for clarity, safety, and ease of use.

---

## 🚀 Features

* Upload prescriptions (PDF)
* Track active/inactive medications
* Generate medication summaries and warnings using Google Gemini
* Semantic drug search with Pinecone
* Support for multiple patient profiles and family management
* Hoverable UI cards showing drug details and interactions

---

## 🧱 Tech Stack

* **Frontend**: React, Material UI, Axios
* **Backend**: FastAPI (Python), Uvicorn, Motor (MongoDB)
* **LLM**: Google Gemini (`gemini-1.5-pro`)
* **Search**: Pinecone + Sentence Transformers (`all-MiniLM-L6-v2`)

---

## 🖥️ Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/sgtanvi/commure.git
cd commure
```

### 2. Set up environment variables

Create a `.env` file in the root of your backend with:

```env
HOST=0.0.0.0
PORT=4000
LOCATION=us-central1
PINECONE_API_KEY= YOUR_API_KEY
GEMINI_API_KEY= YOUR_API_KEY
PINECONE_ENVO=us-east-1
MONGODB_URI=mongodb://localhost:27017
DB_NAME=rxcheck
```

### 3. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Run backend server

```bash
uvicorn backend:app --reload --host localhost --port 4000
```
or

```bash
python backend.py
```
### 5. Start frontend

```bash
cd ../frontend
npm install
npm run dev
```

> React will run on [http://localhost:5173](http://localhost:5173) and FastAPI backend on [http://localhost:4000](http://localhost:4000)

---

## 📂 Project Structure

```
commure/
├── backend/
│   ├── backend.py               # FastAPI app
│   ├── pinecone_query.py        # Drug search logic
│   ├── pinecone_init.py         # Vector index initialization
│   ├── gemini_response.py       # Gemini API integration
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── App.tsx                  # Main routes
│   └── LandingPage.tsx         # Prescription UI & summary
```

