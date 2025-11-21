from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COMPANIES = [
    {"name": "Tata Consultancy Services", "sector": "IT", "country": "India"},
    {"name": "Reliance Industries", "sector": "Energy", "country": "India"},
    {"name": "Infosys", "sector": "IT", "country": "India"},
    {"name": "HDFC Bank", "sector": "Banking", "country": "India"},
    {"name": "Apple Inc", "sector": "Technology", "country": "USA"},
    {"name": "Amazon", "sector": "E-Commerce", "country": "USA"},
]

@app.get("/")
def home():
    return {"message": "Backend working successfully"}

@app.get("/search")
def search_companies(q: str = ""):
    results = [c for c in COMPANIES if q.lower() in c["name"].lower()]
    return {"results": results}
