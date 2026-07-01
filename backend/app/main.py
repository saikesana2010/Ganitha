from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas import SolveRequest, SolveResponse
from app.core.dispatcher import SolverDispatcher
from app.db.session import get_db, init_db
from app.db.cache import get_cached, save_to_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Magine - Math Solver API",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dispatcher = SolverDispatcher()


@app.get("/")
def home():
    return {
        "message": "Magine Backend Running 🚀",
        "version": "2.0.0",
        "supported_types": ["algebra", "calculus", "geometry", "arithmetic", "trigonometry", "statistics", "matrix", "probability", "llm_fallback"]
    }


@app.post("/solve", response_model=SolveResponse)
async def solve_math(request: SolveRequest, db: AsyncSession = Depends(get_db)):
    """
    Solve any math problem with step-by-step explanation.
    Checks cache first, then routes to the appropriate solver.
    """
    # 1. Cache lookup
    cached = await get_cached(db, request.question)
    if cached:
        return cached

    # 2. Solve
    response = await dispatcher.dispatch(request.question)

    # 3. Persist to cache
    await save_to_cache(db, response)

    return response


@app.get("/history")
async def get_history(limit: int = 20, db: AsyncSession = Depends(get_db)):
    """Return recently solved questions from the database."""
    from sqlalchemy import select, desc
    from app.db.models import SolvedQuestion

    result = await db.execute(
        select(SolvedQuestion).order_by(desc(SolvedQuestion.created_at)).limit(limit)
    )
    rows = result.scalars().all()

    return [
        {
            "id": r.id,
            "question": r.question,
            "type": r.type,
            "answer": r.answer,
            "source": r.source,
            "created_at": r.created_at,
        }
        for r in rows
    ]
