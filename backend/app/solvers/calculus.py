import re
from sympy import symbols, diff, integrate, sympify, simplify
from app.solvers.base import BaseSolver
from app.models.schemas import SolveResponse
from typing import List


class CalculusSolver(BaseSolver):

    def solve(self, question: str) -> SolveResponse:
        question_lower = question.lower()

        if any(w in question_lower for w in ["derivative", "differentiate", "d/dx"]):
            return self._solve_derivative(question)

        if any(w in question_lower for w in ["integrate", "integral"]):
            return self._solve_integral(question)

        return SolveResponse(
            type="calculus",
            question=question,
            steps=[],
            answer="",
            error="Could not determine calculus operation (derivative or integral)"
        )

    def _extract_expression(self, question: str) -> str:
        """
        Extract math expression from natural language.
        e.g. "derivative of x^2 + 3x" → "x**2 + 3*x"
        """
        # Remove filler words
        text = re.sub(r"\b(find|the|of|what is|calculate|compute)\b", "", question.lower())
        text = re.sub(r"\b(derivative|differentiate|integrate|integral|with respect to x)\b", "", text)
        text = text.strip()

        # Convert ^ to **
        text = text.replace("^", "**")

        # Convert implicit multiplication: 3x → 3*x
        text = re.sub(r"(\d)([a-z])", r"\1*\2", text)

        return text.strip()

    def _solve_derivative(self, question: str) -> SolveResponse:
        expr_str = self._extract_expression(question)
        x = symbols("x")

        expr = sympify(expr_str)
        derivative = diff(expr, x)
        simplified = simplify(derivative)

        steps = self._derivative_steps(expr, derivative, x)

        return SolveResponse(
            type="calculus",
            question=question,
            steps=steps,
            answer=str(simplified)
        )

    def _solve_integral(self, question: str) -> SolveResponse:
        expr_str = self._extract_expression(question)
        x = symbols("x")

        expr = sympify(expr_str)
        integral = integrate(expr, x)

        steps = [
            f"Given expression: {expr}",
            "Applying integration rules:",
            f"∫ {expr} dx",
            f"= {integral} + C"
        ]

        return SolveResponse(
            type="calculus",
            question=question,
            steps=steps,
            answer=f"{integral} + C"
        )

    def _derivative_steps(self, expr, derivative, x) -> List[str]:
        from sympy import Add, Mul, Pow

        steps = [f"Given expression: f(x) = {expr}"]
        steps.append("Applying differentiation rules:")

        # Break down by terms if it's a sum
        if expr.is_Add:
            terms = expr.as_ordered_terms()
            steps.append(f"Differentiating each term separately:")
            for term in terms:
                term_diff = diff(term, x)
                steps.append(f"  d/dx({term}) = {term_diff}")

        steps.append(f"f'(x) = {derivative}")
        return steps
