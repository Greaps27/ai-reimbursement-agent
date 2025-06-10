from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from thefuzz import fuzz
import os

# Create the FastAPI app
app = FastAPI(
    title="AI Reimbursement Agent API",
    description="Fuzzy search for HRG, ICD-10, and OPCS codes"
)

# CORS configuration
origins = [
    "http://localhost:5173",
    "https://ai-reimbursement-agent.vercel.app",
    "https://*.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Point to your CSV files in backend/data/
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Load all 3 datasets
def load_data():
    return {
        "HRG Codes": pd.read_csv(os.path.join(DATA_DIR, "hrg_codes.csv")),
        "ICD-10 Codes": pd.read_csv(os.path.join(DATA_DIR, "icd10_codes.csv")),
        "OPCS Codes": pd.read_csv(os.path.join(DATA_DIR, "opcs_codes.csv")),
    }

# Fuzzy match your query to the datasets
def search_data(query, threshold=80):
    datasets = load_data()
    result = {}
    for name, df in datasets.items():
        matches = []
        for _, row in df.iterrows():
            row_text = " | ".join([str(v) if pd.notna(v) else "" for v in row.values])
            score = fuzz.partial_ratio(query.lower(), row_text.lower())
            if score >= threshold:
                matches.append({"score": score, "text": row_text})
        result[name] = sorted(matches, key=lambda x: x["score"], reverse=True)[:5]
    return result

# 👋 Welcome message
@app.get("/")
def read_root():
    return {"message": "AI Reimbursement Agent API is running."}

# 🔍 Search endpoint
@app.post("/search")
async def search(request: Request):
    try:
        body = await request.json()
        query = body.get("query", "")
        if not query:
            raise HTTPException(status_code=400, detail="Missing query")

        results = search_data(query)
        return results

    except Exception as e:
        print("❌ REAL ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Search error")
