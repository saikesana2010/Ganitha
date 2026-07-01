import math
from app.solvers.base import BaseSolver
from app.models.schemas import SolveResponse
from app.core.parser import MathParser
from typing import List, Optional


class GeometrySolver(BaseSolver):

    def solve(self, question: str) -> SolveResponse:
        question_lower = question.lower()
        params = MathParser.extract_geometry_params(question)

        if not params:
            return SolveResponse(
                type="geometry",
                question=question,
                steps=[],
                answer="",
                error="Could not extract geometry parameters from input"
            )

        shape = params.get("shape")

        # Area
        if "area" in question_lower:
            return self._solve_area(question, shape, params)

        # Perimeter
        if "perimeter" in question_lower:
            return self._solve_perimeter(question, shape, params)

        # Volume
        if "volume" in question_lower:
            return self._solve_volume(question, shape, params)

        # Circumference
        if "circumference" in question_lower:
            return self._solve_circumference(question, params)

        return SolveResponse(
            type="geometry",
            question=question,
            steps=[],
            answer="",
            error="Unsupported geometry operation"
        )

    def _solve_area(self, question: str, shape: Optional[str], params: dict) -> SolveResponse:
        if shape == "circle":
            r = params.get("radius")
            if r is None:
                return self._missing_param("radius")
            area = math.pi * r * r
            steps = [
                f"Given: radius r = {r}",
                "Formula: Area = π × r²",
                f"Area = π × {r}²",
                f"Area = π × {r * r}",
                f"Area = {area:.4f}"
            ]
            return SolveResponse(type="geometry", question=question, steps=steps, answer=f"{area:.4f}")

        if shape == "rectangle":
            l = params.get("length")
            w = params.get("width")
            if l is None or w is None:
                return self._missing_param("length and width")
            area = l * w
            steps = [
                f"Given: length = {l}, width = {w}",
                "Formula: Area = length × width",
                f"Area = {l} × {w}",
                f"Area = {area}"
            ]
            return SolveResponse(type="geometry", question=question, steps=steps, answer=str(area))

        if shape == "triangle":
            b = params.get("length")
            h = params.get("height")
            if b is None or h is None:
                return self._missing_param("base (length) and height")
            area = 0.5 * b * h
            steps = [
                f"Given: base = {b}, height = {h}",
                "Formula: Area = ½ × base × height",
                f"Area = ½ × {b} × {h}",
                f"Area = {area}"
            ]
            return SolveResponse(type="geometry", question=question, steps=steps, answer=str(area))

        if shape == "square":
            s = params.get("length")
            if s is None:
                return self._missing_param("side length")
            area = s * s
            steps = [
                f"Given: side = {s}",
                "Formula: Area = side²",
                f"Area = {s}² = {area}"
            ]
            return SolveResponse(type="geometry", question=question, steps=steps, answer=str(area))

        return SolveResponse(
            type="geometry", question=question, steps=[], answer="",
            error=f"Area formula not available for shape: {shape}"
        )

    def _solve_perimeter(self, question: str, shape: Optional[str], params: dict) -> SolveResponse:
        if shape == "circle":
            r = params.get("radius")
            if r is None:
                return self._missing_param("radius")
            perimeter = 2 * math.pi * r
            steps = [
                f"Given: radius r = {r}",
                "Formula: Circumference = 2 × π × r",
                f"= 2 × π × {r}",
                f"= {perimeter:.4f}"
            ]
            return SolveResponse(type="geometry", question=question, steps=steps, answer=f"{perimeter:.4f}")

        if shape == "rectangle":
            l = params.get("length")
            w = params.get("width")
            if l is None or w is None:
                return self._missing_param("length and width")
            perimeter = 2 * (l + w)
            steps = [
                f"Given: length = {l}, width = {w}",
                "Formula: Perimeter = 2 × (length + width)",
                f"= 2 × ({l} + {w})",
                f"= {perimeter}"
            ]
            return SolveResponse(type="geometry", question=question, steps=steps, answer=str(perimeter))

        if shape == "square":
            s = params.get("length")
            if s is None:
                return self._missing_param("side length")
            perimeter = 4 * s
            steps = [
                f"Given: side = {s}",
                "Formula: Perimeter = 4 × side",
                f"= 4 × {s} = {perimeter}"
            ]
            return SolveResponse(type="geometry", question=question, steps=steps, answer=str(perimeter))

        return SolveResponse(
            type="geometry", question=question, steps=[], answer="",
            error=f"Perimeter formula not available for shape: {shape}"
        )

    def _solve_volume(self, question: str, shape: Optional[str], params: dict) -> SolveResponse:
        if shape == "circle":  # sphere
            r = params.get("radius")
            if r is None:
                return self._missing_param("radius")
            volume = (4 / 3) * math.pi * r ** 3
            steps = [
                f"Given: radius r = {r}",
                "Formula: Volume of sphere = (4/3) × π × r³",
                f"= (4/3) × π × {r}³",
                f"= {volume:.4f}"
            ]
            return SolveResponse(type="geometry", question=question, steps=steps, answer=f"{volume:.4f}")

        return SolveResponse(
            type="geometry", question=question, steps=[], answer="",
            error=f"Volume formula not available for shape: {shape}"
        )

    def _solve_circumference(self, question: str, params: dict) -> SolveResponse:
        r = params.get("radius")
        if r is None:
            return self._missing_param("radius")
        c = 2 * math.pi * r
        steps = [
            f"Given: radius r = {r}",
            "Formula: Circumference = 2 × π × r",
            f"= 2 × π × {r}",
            f"= {c:.4f}"
        ]
        return SolveResponse(type="geometry", question=question, steps=steps, answer=f"{c:.4f}")

    def _missing_param(self, param: str) -> SolveResponse:
        return SolveResponse(
            type="geometry", question="", steps=[], answer="",
            error=f"Missing required parameter: {param}"
        )
