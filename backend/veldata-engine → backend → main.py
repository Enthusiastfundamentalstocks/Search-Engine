from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import csv
from pathlib import Path

app = FastAPI(title="VELDATA Investment Engine - MVP")

DATA_FILE = Path(__file__).parent / "data" / "listed_companies_sample.csv"

class SearchRequest(BaseModel):
    query: Optional[str] = None
    min_roe: Optional[float] = None
    max_de_ratio: Optional[float] = None
    limit: int = 20
    offset: int = 0

class CompanyOut(BaseModel):
    name: str
    ticker: str
    exchange: str
    sector: str
    market_cap: Optional[float]
    roe: Optional[float]
    sales_cagr_3y: Optional[float]
    debt_to_equity: Optional[float]
    pe: Optional[float]
    promoter_holding: Optional[float]
    veldata_score: float

COMPANIES = []

def _safe_float(val):
    try:
        return float(val)
    except:
        return None

def compute_veldata(row):
    roe = _safe_float(row.get("roe", ""))
    growth = _safe_float(row.get("sales_cagr_3y", ""))
    de = _safe_float(row.get("debt_to_equity", ""))
    promoter = _safe_float(row.get("promoter_holding", ""))

    roe_score = min(max((roe or 10) / 30, 0), 1)
    growth_score = min(max((growth or 5) / 20, 0), 1)
    debt_score = 1 - min(max((de or 1) / 2, 0), 1)
    promoter_score = min(max((promoter or 30) / 80, 0), 1)

    veldata = (
        0.3 * roe_score +
        0.25 * growth_score +
        0.2 * debt_score +
        0.25 * promoter_score
    )

    return round(veldata * 100, 2)

def load_data():
    global COMPANIES
    with open(DATA_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        COMPANIES = []
        for row in reader:
            row["veldata_score"] = compute_veldata(row)
            COMPANIES.append(row)

@app.on_event("startup")
def startup():
    load_data()

@app.post("/search", response_model=List[CompanyOut])
def search(req: SearchRequest):
    results = COMPANIES

    if req.query:
        q = req.query.lower()
        results = [r for r in results if q in r["name"].lower() or q in r["sector"].lower()]

    if req.min_roe is not None:
        results = [r for r in results if _safe_float(r["roe"]) >= req.min_roe]

    if req.max_de_ratio is not None:
        results = [r for r in results if _safe_float(r["debt_to_equity"]) <= req.max_de_ratio]

    results = sorted(results, key=lambda x: x["veldata_score"], reverse=True)
    return results[req.offset:req.offset + req.limit]
