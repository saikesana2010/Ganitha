from sympy import symbols, Eq, solve, sympify
from sympy import expand, factor, simplify
from app.solvers.base import BaseSolver
from app.models.schemas import SolveResponse
from app.core.parser import MathParser
from typing import List


class AlgebraSolver(BaseSolver):

    def solve(self, question: str) -> SolveResponse:
        equation_parts = MathParser.extract_equation(question)

        if not equation_parts:
            return SolveResponse(
                type="algebra",
                question=question,
                steps=[],
                answer="",
                error="Could not extract equation from input"
            )

        left_str = equation_parts["left"]
        right_str = equation_parts["right"]

        x = symbols("x")

        left_expr = sympify(left_str)
        right_expr = sympify(right_str)

        equation = Eq(left_expr, right_expr)
        result = solve(equation, x)

        steps = self._generate_steps(left_expr, right_expr, equation, result, x)

        return SolveResponse(
            type="algebra",
            question=question,
            steps=steps,
            answer=str(result)
        )

    def _generate_steps(self, left_expr, right_expr, equation, result, x) -> List[str]:
        steps = []

        steps.append(f"Given equation: {left_expr} = {right_expr}")

        # Move everything to left side
        combined = left_expr - right_expr
        expanded = expand(combined)
        steps.append(f"Rearranging: {expanded} = 0")

        # Check if quadratic
        degree = expanded.as_poly(x).degree() if expanded.as_poly(x) else 1

        if degree == 2:
            steps.append("This is a quadratic equation. Solving using the quadratic formula or factoring.")
            factored = factor(expanded)
            if factored != expanded:
                steps.append(f"Factored form: {factored} = 0")

        elif degree == 1:
            steps.append("This is a linear equation. Isolating x.")

        # Collect terms
        steps.append(f"Solving for x:")

        if result:
            for r in result:
                steps.append(f"  x = {r}")
        else:
            steps.append("  No real solution found")

        return steps
