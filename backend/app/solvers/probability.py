import re
import math
from app.solvers.base import BaseSolver
from app.models.schemas import SolveResponse


class ProbabilitySolver(BaseSolver):

    def solve(self, question: str) -> SolveResponse:
        q = question.lower()

        if "combination" in q or " ncr " in q or "c(" in q:
            return self._combination(question)
        if "permutation" in q or " npr " in q or "p(" in q:
            return self._permutation(question)
        if "probability" in q or "p(" in q:
            return self._probability(question)
        if "factorial" in q or "!" in question:
            return self._factorial(question)

        return SolveResponse(
            type="probability", question=question, steps=[], answer="",
            error="Specify operation: combination, permutation, probability, or factorial"
        )

    # ------------------------------------------------------------------ #

    def _combination(self, question: str) -> SolveResponse:
        n, r = self._extract_two_numbers(question)
        if n is None:
            return self._parse_error(question)
        n, r = int(n), int(r)
        if r > n:
            return SolveResponse(type="probability", question=question, steps=[], answer="",
                                 error="r cannot be greater than n in C(n,r)")
        result = math.comb(n, r)
        steps = [
            f"C({n}, {r}) = n! / (r! × (n-r)!)",
            f"= {n}! / ({r}! × {n-r}!)",
            f"= {math.factorial(n)} / ({math.factorial(r)} × {math.factorial(n-r)})",
            f"= {result}"
        ]
        return SolveResponse(type="probability", question=question, steps=steps, answer=str(result))

    def _permutation(self, question: str) -> SolveResponse:
        n, r = self._extract_two_numbers(question)
        if n is None:
            return self._parse_error(question)
        n, r = int(n), int(r)
        if r > n:
            return SolveResponse(type="probability", question=question, steps=[], answer="",
                                 error="r cannot be greater than n in P(n,r)")
        result = math.perm(n, r)
        steps = [
            f"P({n}, {r}) = n! / (n-r)!",
            f"= {n}! / {n-r}!",
            f"= {math.factorial(n)} / {math.factorial(n-r)}",
            f"= {result}"
        ]
        return SolveResponse(type="probability", question=question, steps=steps, answer=str(result))

    def _probability(self, question: str) -> SolveResponse:
        # Pattern: "X out of Y" or "X/Y"
        match = re.search(r'(\d+)\s*(?:out of|/)\s*(\d+)', question.lower())
        if match:
            favourable = int(match.group(1))
            total = int(match.group(2))
            prob = favourable / total
            steps = [
                f"Favourable outcomes = {favourable}",
                f"Total outcomes = {total}",
                f"P(event) = favourable / total",
                f"= {favourable} / {total}",
                f"= {prob:.6f}"
            ]
            return SolveResponse(type="probability", question=question, steps=steps, answer=f"{prob:.6f}")

        return self._parse_error(question)

    def _factorial(self, question: str) -> SolveResponse:
        match = re.search(r'(\d+)\s*!', question)
        if not match:
            match = re.search(r'factorial\s+of\s+(\d+)', question.lower())
        if not match:
            return self._parse_error(question)
        n = int(match.group(1))
        if n > 20:
            return SolveResponse(type="probability", question=question, steps=[], answer="",
                                 error="Factorial too large to display step-by-step (n > 20)")
        result = math.factorial(n)
        expansion = " × ".join(str(i) for i in range(n, 0, -1))
        steps = [
            f"{n}! = {expansion}",
            f"= {result}"
        ]
        return SolveResponse(type="probability", question=question, steps=steps, answer=str(result))

    # ------------------------------------------------------------------ #

    def _extract_two_numbers(self, question: str):
        nums = re.findall(r'\d+', question)
        if len(nums) >= 2:
            return float(nums[0]), float(nums[1])
        return None, None

    def _parse_error(self, question: str) -> SolveResponse:
        return SolveResponse(
            type="probability", question=question, steps=[], answer="",
            error="Could not parse the problem. Example: 'combination 5 3' or '3 out of 10'"
        )
