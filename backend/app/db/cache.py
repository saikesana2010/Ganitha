from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import SolvedQuestion
from app.models.schemas import SolveResponse
from typing import Optional
import re


def _normalize_for_match(text: str) -> str:
    """Strip punctuation/spaces/case for fuzzy comparison."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '', text)
    return text


async def get_cached(db: AsyncSession, question: str) -> Optional[SolveResponse]:
    """Exact match first, then fuzzy match on normalized question."""
    # 1. Exact match
    result = await db.execute(
        select(SolvedQuestion).where(SolvedQuestion.question == question)
    )
    row = result.scalars().first()
    if row:
        return _to_response(row, "cache")

    # 2. Fuzzy match — compare normalized strings
    normalized_input = _normalize_for_match(question)
    all_rows = await db.execute(select(SolvedQuestion))
    for row in all_rows.scalars().all():
        if _normalize_for_match(row.question) == normalized_input:
            return _to_response(row, "cache")

    return None


async def save_to_cache(db: AsyncSession, response: SolveResponse) -> None:
    """Persist a solved question to the database."""
    if response.error:
        return
    record = SolvedQuestion(
        question=response.question,
        type=response.type,
        steps=response.steps,
        answer=response.answer,
        source=response.source
    )
    db.add(record)
    await db.commit()


def _to_response(row: SolvedQuestion, source: str) -> SolveResponse:
    return SolveResponse(
        type=row.type,
        question=row.question,
        steps=row.steps,
        answer=row.answer,
        source=source
    )
