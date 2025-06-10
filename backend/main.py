from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from thefuzz import fuzz
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_data():
    return {
        "HRG Codes": pd.read_csv(f"{DATA_DIR}/hrg_codes.csv"),
        "ICD-10 Codes": pd.read_csv(f"{DATA_DIR}/icd10_codes.csv"),
        "OPCS Codes": pd.read_csv(f"{DATA_DIR}/opcs_codes.csv"),
    }

def search_data(query, threshold=80):
    datasets = load_data()
    result = {}
    for name, df in datasets.items():
        matches = []
        for _, row in df.iterrows():
            row_text = " | ".join(map(str, row.values))
            score = fuzz.partial_ratio(query.lower(), row_text.lower())
            if score >= threshold:
                matches.append({"score": score, "text": row_text})
        result[name] = sorted(matches, key=lambda x: x["score"], reverse=True)[:5]
    return result

@app.post("/search")
async def search(request: Request):
    body = await request.json()
    query = body.get("query", "")
    if not query:
        raise HTTPException(status_code=400, detail="Missing query")
    return search_data(query)
