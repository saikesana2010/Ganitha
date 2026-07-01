import os
import httpx
from app.models.schemas import SolveResponse


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-math:1.5b")

MATH_PROMPT_TEMPLATE = """You are a mathematics tutor. Solve the following problem step by step.

Problem: {question}

Instructions:
- Identify the type of problem
- Show every step clearly
- State the final answer at the end in the format: ANSWER: <value>

Solution:"""


async def solve_with_llm(question: str) -> SolveResponse:
    prompt = MATH_PROMPT_TEMPLATE.format(question=question)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            data = response.json()

        raw_text: str = data.get("response", "")
        steps, answer = _parse_llm_response(raw_text)

        return SolveResponse(
            type="llm",
            question=question,
            steps=steps,
            answer=answer,
            source="llm"
        )

    except httpx.ConnectError:
        return SolveResponse(
            type="unknown",
            question=question,
            steps=[],
            answer="",
            source="llm",
            error="Ollama is not running. Start it with: ollama serve"
        )
    except Exception as e:
        return SolveResponse(
            type="unknown",
            question=question,
            steps=[],
            answer="",
            source="llm",
            error=f"LLM error: {str(e)}"
        )


def _parse_llm_response(text: str):
    """
    Split LLM response into steps list and final answer.
    """
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    answer = ""
    steps = []

    for line in lines:
        if line.upper().startswith("ANSWER:"):
            answer = line.split(":", 1)[-1].strip()
        else:
            steps.append(line)

    if not answer and steps:
        answer = steps[-1]

    return steps, answer
