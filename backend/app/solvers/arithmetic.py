import re
from fractions import Fraction
from app.solvers.base import BaseSolver
from app.models.schemas import SolveResponse
from typing import List


class ArithmeticSolver(BaseSolver):

    def solve(self, question: str) -> SolveResponse:
        question_lower = question.lower()

        if "%" in question or "percent" in question_lower:
            return self._solve_percentage(question)

        if "/" in question and "=" not in question:
            return self._solve_fraction(question)

        return self._solve_expression(question)

    # ------------------------------------------------------------------ #
    #  Expression evaluator (BODMAS)                                       #
    # ------------------------------------------------------------------ #
    def _solve_expression(self, question: str) -> SolveResponse:
        expr = self._extract_expression(question)

        try:
            steps = self._bodmas_steps(expr)
            result = self._safe_eval(expr)
            steps.append(f"Result = {result}")

            return SolveResponse(
                type="arithmetic",
                question=question,
                steps=steps,
                answer=str(result)
            )
        except Exception:
            return SolveResponse(
                type="arithmetic",
                question=question,
                steps=[],
                answer="",
                error="Could not evaluate arithmetic expression"
            )

    def _bodmas_steps(self, expr: str) -> List[str]:
        steps = [f"Expression: {expr}", "Applying BODMAS order of operations:"]

        # Show bracket resolution
        bracket_match = re.search(r'\(([^()]+)\)', expr)
        if bracket_match:
            inner = bracket_match.group(1)
            inner_val = self._safe_eval(inner)
            steps.append(f"  Brackets: ({inner}) = {inner_val}")

        # Show exponent
        if "**" in expr or "^" in expr:
            steps.append("  Applying exponents (Orders)")

        # Show division/multiplication
        if "*" in expr or "/" in expr:
            steps.append("  Applying multiplication / division (left to right)")

        # Show addition/subtraction
        if "+" in expr or re.search(r'(?<!\*)-', expr):
            steps.append("  Applying addition / subtraction (left to right)")

        return steps

    # ------------------------------------------------------------------ #
    #  Fraction solver                                                     #
    # ------------------------------------------------------------------ #
    def _solve_fraction(self, question: str) -> SolveResponse:
        expr = self._extract_expression(question)

        try:
            # Use Python's Fraction for exact arithmetic
            result = Fraction(expr).limit_denominator(1000)
            steps = [
                f"Expression: {expr}",
                "Converting to fraction form:",
                f"= {result}",
            ]
            if result.denominator == 1:
                steps.append(f"Simplified: {result.numerator}")
                answer = str(result.numerator)
            else:
                steps.append(f"Simplified: {result.numerator}/{result.denominator}")
                answer = f"{result.numerator}/{result.denominator}"

            return SolveResponse(type="arithmetic", question=question, steps=steps, answer=answer)
        except Exception:
            return self._solve_expression(question)

    # ------------------------------------------------------------------ #
    #  Percentage solver                                                   #
    # ------------------------------------------------------------------ #
    def _solve_percentage(self, question: str) -> SolveResponse:
        question_lower = question.lower()

        # Pattern: "X% of Y"
        match = re.search(r'(\d+\.?\d*)\s*%\s*of\s*(\d+\.?\d*)', question_lower)
        if match:
            percent = float(match.group(1))
            total = float(match.group(2))
            result = (percent / 100) * total
            steps = [
                f"Find {percent}% of {total}",
                f"Formula: (percent / 100) × total",
                f"= ({percent} / 100) × {total}",
                f"= {percent / 100} × {total}",
                f"= {result}"
            ]
            return SolveResponse(type="arithmetic", question=question, steps=steps, answer=str(result))

        # Pattern: "what percent is X of Y"
        match2 = re.search(r'what percent.*?(\d+\.?\d*).*?of\s*(\d+\.?\d*)', question_lower)
        if match2:
            part = float(match2.group(1))
            whole = float(match2.group(2))
            result = (part / whole) * 100
            steps = [
                f"Find what percent {part} is of {whole}",
                f"Formula: (part / whole) × 100",
                f"= ({part} / {whole}) × 100",
                f"= {result:.2f}%"
            ]
            return SolveResponse(type="arithmetic", question=question, steps=steps, answer=f"{result:.2f}%")

        return SolveResponse(
            type="arithmetic", question=question, steps=[], answer="",
            error="Could not parse percentage problem"
        )

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #
    def _extract_expression(self, question: str) -> str:
        text = question.lower()
        text = re.sub(r'\b(what is|calculate|find|compute|evaluate|simplify)\b', '', text)
        text = text.replace("^", "**")
        text = text.replace("x", "*")
        text = text.strip()
        # Keep only valid math characters
        text = re.sub(r'[^\d\s\+\-\*\/\.\(\)\%\*]', '', text)
        return text.strip()

    def _safe_eval(self, expr: str):
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expr):
            raise ValueError("Invalid characters in expression")
        return eval(compile(expr, "<string>", "eval"), {"__builtins__": {}})
