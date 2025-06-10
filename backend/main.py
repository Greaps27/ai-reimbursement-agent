from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from thefuzz import fuzz, process
from pydantic import BaseModel

app = FastAPI(
    title="AI Reimbursement Agent API",
    description="Fuzzy matching API for HRG, ICD-10, OPCS codes"
)

# ✅ CORS Setup
origins = [
    "http://localhost:5173",
    "https://ai-reimbursement-agent.vercel.app",
    "https://*.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load data
def load_data():
    hrg = pd.read_csv("data/hrg_codes.csv")
    icd = pd.read_csv("data/icd10_codes.csv")
    opcs = pd.read_csv("data/opcs_codes.csv")
    return {"HRG Codes": hrg, "ICD-10 Codes": icd, "OPCS Codes": opcs}

# ✅ Search logic
def search_data(query: str, threshold=80):
    datasets = load_data()
    results = {}
    for name, df in datasets.items():
        matches = []
        for _, row in df.iterrows():
            row_text = " ".join(row.astype(str).values)
            score = fuzz.partial_ratio(query.lower(), row_text.lower())
            if score >= threshold:
                matches.append({"score": score, "text": row_text})
        results[name] = sorted(matches, key=lambda x: x["score"], reverse=True)[:5]
    return results

# ✅ Root route
@app.get("/")
def read_root():
    return {"message": "AI Reimbursement Agent API"}

# ✅ POST /search
@app.post("/search")
async def search(request: Request):
    try:
        body = await request.json()
        query = body.get("query", "")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required.")
        results = search_data(query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
