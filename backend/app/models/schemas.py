from pydantic import BaseModel
from typing import List, Optional


class SolveRequest(BaseModel):
    question: str


class SolveResponse(BaseModel):
    type: str
    question: str
    steps: List[str]
    answer: str
    source: str = "engine"          # "engine" | "llm"
    error: Optional[str] = None
