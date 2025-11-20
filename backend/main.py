from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

# This is our in-memory database
database = []

# Schema for input data
class Company(BaseModel):
    name: str
    description: str
    sector: str
    funding_stage: str
    location: str
    keywords: List[str] = []


@app.get("/")
def home():
    return {"message": "Search Engine Backend Running"}


# -------- 1) INDEX API -----------
@app.post("/index")
def index_company(company: Company):
    database.append(company.dict())
    return {"status": "success", "total_companies": len(database)}


# -------- 2) SEARCH API ----------
@app.get("/search")
def search(q: str):
    q = q.lower()
    results = []

    for company in database:
        text = (
            company["name"] + " " +
            company["description"] + " " +
            company["sector"] + " " +
            company["funding_stage"] + " " +
            company["location"] + " " +
            " ".join(company["keywords"])
        ).lower()

        if re.search(q, text):
            results.append(company)

    return {"query": q, "results_found": len(results), "results": results}

