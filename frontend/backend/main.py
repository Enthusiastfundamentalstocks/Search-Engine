from fastapi import FastAPI

app = FastAPI()

COMPANIES = [
    "Apple",
    "Google",
    "Microsoft",
    "Amazon",
    "Netflix",
    "Uber"
]

@app.get("/")
def home():
    return {"message": "Backend working successfully"}

@app.get("/search")
def search_companies(q: str = ""):
    results = [c for c in COMPANIES if q.lower() in c.lower()]
    return {"results": results}
