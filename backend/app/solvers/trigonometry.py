import re
import math
from sympy import symbols, sin, cos, tan, asin, acos, atan, pi, simplify, trigsimp, sympify
from sympy import sec, csc, cot
from app.solvers.base import BaseSolver
from app.models.schemas import SolveResponse
from typing import List, Optional


TRIG_EXACT = {
    0:   {"sin": "0",       "cos": "1",         "tan": "0"},
    30:  {"sin": "1/2",     "cos": "√3/2",      "tan": "1/√3"},
    45:  {"sin": "1/√2",    "cos": "1/√2",      "tan": "1"},
    60:  {"sin": "√3/2",    "cos": "1/2",       "tan": "√3"},
    90:  {"sin": "1",       "cos": "0",         "tan": "undefined"},
    180: {"sin": "0",       "cos": "-1",        "tan": "0"},
    270: {"sin": "-1",      "cos": "0",         "tan": "undefined"},
    360: {"sin": "0",       "cos": "1",         "tan": "0"},
}


class TrigonometrySolver(BaseSolver):

    def solve(self, question: str) -> SolveResponse:
        question_lower = question.lower()

        func, angle, unit = self._parse_trig(question_lower)

        if func and angle is not None:
            return self._evaluate_trig(question, func, angle, unit)

        # Identity simplification
        if "simplify" in question_lower or "identity" in question_lower:
            return self._simplify_expression(question)

        return SolveResponse(
            type="trigonometry",
            question=question,
            steps=[],
            answer="",
            error="Could not parse trigonometric expression"
        )

    # ------------------------------------------------------------------ #
    #  Parse trig function and angle                                       #
    # ------------------------------------------------------------------ #
    def _parse_trig(self, text: str):
        func_map = {
            "sin": "sin", "cos": "cos", "tan": "tan",
            "sec": "sec", "cosec": "csc", "csc": "csc", "cot": "cot",
            "arcsin": "asin", "arccos": "acos", "arctan": "atan",
            "asin": "asin", "acos": "acos", "atan": "atan",
        }

        func = None
        for key, val in func_map.items():
            if key in text:
                func = val
                break

        if func is None:
            return None, None, None

        # Extract angle value
        angle_match = re.search(r'(\d+\.?\d*)\s*(degree|degrees|deg|°|radian|radians|rad)?', text)
        if not angle_match:
            return func, None, None

        angle = float(angle_match.group(1))
        unit_str = angle_match.group(2) or ""
        unit = "radian" if "rad" in unit_str else "degree"

        return func, angle, unit

    # ------------------------------------------------------------------ #
    #  Evaluate trig function                                              #
    # ------------------------------------------------------------------ #
    def _evaluate_trig(self, question: str, func: str, angle: float, unit: str) -> SolveResponse:
        steps = []

        if unit == "degree":
            steps.append(f"Given: {func}({angle}°)")
            steps.append(f"Converting to radians: {angle}° × (π/180) = {math.radians(angle):.6f} rad")
            angle_rad = math.radians(angle)
        else:
            steps.append(f"Given: {func}({angle} rad)")
            angle_rad = angle

        # Check exact value table
        if unit == "degree" and int(angle) in TRIG_EXACT and func in ("sin", "cos", "tan"):
            exact = TRIG_EXACT[int(angle)].get(func)
            steps.append(f"From standard values table: {func}({int(angle)}°) = {exact}")
            if exact == "undefined":
                return SolveResponse(type="trigonometry", question=question, steps=steps, answer="undefined")
            steps.append(f"Decimal approximation: {self._compute(func, angle_rad):.6f}")
            return SolveResponse(
                type="trigonometry", question=question, steps=steps,
                answer=f"{exact} ≈ {self._compute(func, angle_rad):.6f}"
            )

        result = self._compute(func, angle_rad)
        steps.append(f"Applying {func} function:")
        steps.append(f"{func}({angle_rad:.6f}) = {result:.6f}")

        return SolveResponse(
            type="trigonometry", question=question, steps=steps, answer=f"{result:.6f}"
        )

    def _compute(self, func: str, angle_rad: float) -> float:
        fn_map = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "sec": lambda a: 1 / math.cos(a),
            "csc": lambda a: 1 / math.sin(a),
            "cot": lambda a: math.cos(a) / math.sin(a),
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
        }
        return fn_map[func](angle_rad)

    # ------------------------------------------------------------------ #
    #  Simplify trig expression                                            #
    # ------------------------------------------------------------------ #
    def _simplify_expression(self, question: str) -> SolveResponse:
        text = re.sub(r'\b(simplify|the|expression|identity)\b', '', question.lower()).strip()
        text = text.replace("^", "**")
        text = re.sub(r'(\d)([a-z])', r'\1*\2', text)

        x = symbols("x")
        try:
            expr = sympify(text)
            simplified = trigsimp(expr)
            steps = [
                f"Given expression: {expr}",
                "Applying trigonometric identities:",
                f"Simplified: {simplified}"
            ]
            return SolveResponse(
                type="trigonometry", question=question, steps=steps, answer=str(simplified)
            )
        except Exception:
            return SolveResponse(
                type="trigonometry", question=question, steps=[], answer="",
                error="Could not simplify trigonometric expression"
            )
