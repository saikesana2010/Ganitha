import re
from sympy import Matrix
from app.solvers.base import BaseSolver
from app.models.schemas import SolveResponse


class MatrixSolver(BaseSolver):

    def solve(self, question: str) -> SolveResponse:
        q = question.lower()

        if "determinant" in q or "det" in q:
            return self._determinant(question)
        if "transpose" in q:
            return self._transpose(question)
        if "inverse" in q:
            return self._inverse(question)
        if "multiply" in q or "product" in q:
            return self._multiply(question)
        if "add" in q or "sum" in q:
            return self._add(question)

        return SolveResponse(
            type="matrix", question=question, steps=[], answer="",
            error="Specify operation: determinant, transpose, inverse, multiply, or add"
        )

    # ------------------------------------------------------------------ #

    def _parse_matrices(self, question: str):
        """Extract all matrices from input like [[1,2],[3,4]]"""
        raw = re.findall(r'\[\s*(?:\[[\d\s,\-\.]+\]\s*,?\s*)+\]', question)
        matrices = []
        for r in raw:
            try:
                rows = re.findall(r'\[([\d\s,\-\.]+)\]', r)
                matrix = [[float(x) for x in row.split(',')] for row in rows]
                matrices.append(Matrix(matrix))
            except Exception:
                continue
        return matrices

    def _determinant(self, question: str) -> SolveResponse:
        matrices = self._parse_matrices(question)
        if not matrices:
            return self._parse_error(question)
        M = matrices[0]
        if M.shape[0] != M.shape[1]:
            return SolveResponse(type="matrix", question=question, steps=[], answer="",
                                 error="Determinant requires a square matrix")
        det = M.det()
        steps = [
            f"Given matrix: {self._fmt(M)}",
            f"Matrix size: {M.shape[0]}×{M.shape[1]}",
            f"Calculating determinant using cofactor expansion:",
            f"det(A) = {det}"
        ]
        return SolveResponse(type="matrix", question=question, steps=steps, answer=str(det))

    def _transpose(self, question: str) -> SolveResponse:
        matrices = self._parse_matrices(question)
        if not matrices:
            return self._parse_error(question)
        M = matrices[0]
        T = M.T
        steps = [
            f"Given matrix A: {self._fmt(M)}",
            "Transpose: swap rows and columns",
            f"Aᵀ = {self._fmt(T)}"
        ]
        return SolveResponse(type="matrix", question=question, steps=steps, answer=self._fmt(T))

    def _inverse(self, question: str) -> SolveResponse:
        matrices = self._parse_matrices(question)
        if not matrices:
            return self._parse_error(question)
        M = matrices[0]
        if M.det() == 0:
            return SolveResponse(type="matrix", question=question, steps=[], answer="",
                                 error="Matrix is singular (determinant = 0), inverse does not exist")
        inv = M.inv()
        steps = [
            f"Given matrix A: {self._fmt(M)}",
            f"det(A) = {M.det()} ≠ 0, so inverse exists",
            f"A⁻¹ = {self._fmt(inv)}"
        ]
        return SolveResponse(type="matrix", question=question, steps=steps, answer=self._fmt(inv))

    def _multiply(self, question: str) -> SolveResponse:
        matrices = self._parse_matrices(question)
        if len(matrices) < 2:
            return self._parse_error(question)
        A, B = matrices[0], matrices[1]
        if A.shape[1] != B.shape[0]:
            return SolveResponse(type="matrix", question=question, steps=[], answer="",
                                 error=f"Cannot multiply: columns of A ({A.shape[1]}) ≠ rows of B ({B.shape[0]})")
        result = A * B
        steps = [
            f"Matrix A: {self._fmt(A)}",
            f"Matrix B: {self._fmt(B)}",
            f"A × B = {self._fmt(result)}"
        ]
        return SolveResponse(type="matrix", question=question, steps=steps, answer=self._fmt(result))

    def _add(self, question: str) -> SolveResponse:
        matrices = self._parse_matrices(question)
        if len(matrices) < 2:
            return self._parse_error(question)
        A, B = matrices[0], matrices[1]
        if A.shape != B.shape:
            return SolveResponse(type="matrix", question=question, steps=[], answer="",
                                 error="Matrices must have the same dimensions to add")
        result = A + B
        steps = [
            f"Matrix A: {self._fmt(A)}",
            f"Matrix B: {self._fmt(B)}",
            f"A + B = {self._fmt(result)}"
        ]
        return SolveResponse(type="matrix", question=question, steps=steps, answer=self._fmt(result))

    def _fmt(self, M: Matrix) -> str:
        return str(M.tolist())

    def _parse_error(self, question: str) -> SolveResponse:
        return SolveResponse(
            type="matrix", question=question, steps=[], answer="",
            error="Could not parse matrix. Use format: [[1,2],[3,4]]"
        )
