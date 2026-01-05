from fastapi import FastAPI
from pydantic import BaseModel
from search import semantic_search

app = FastAPI()

print("DEBUG: api.py loaded")

class SearchRequest(BaseModel):
    query: str
    domain: str | None = None
    top_k: int = 3

@app.post("/search")
def search_endpoint(req: SearchRequest):
    print("DEBUG: /search endpoint hit")
    result = semantic_search(
        query=req.query,
        top_k=req.top_k,
        domain=req.domain
    )

    print("DEBUG: semantic_search returned ->", result)
    
    return result
