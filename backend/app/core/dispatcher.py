import asyncio
from app.core.parser import MathParser
from app.solvers.algebra import AlgebraSolver
from app.solvers.calculus import CalculusSolver
from app.solvers.geometry import GeometrySolver
from app.solvers.arithmetic import ArithmeticSolver
from app.solvers.trigonometry import TrigonometrySolver
from app.solvers.statistics import StatisticsSolver
from app.solvers.matrix import MatrixSolver
from app.solvers.probability import ProbabilitySolver
from app.models.schemas import SolveResponse
from app.llm.ollama_client import solve_with_llm


class SolverDispatcher:

    def __init__(self):
        self.solvers = {
            "algebra":      AlgebraSolver(),
            "calculus":     CalculusSolver(),
            "geometry":     GeometrySolver(),
            "arithmetic":   ArithmeticSolver(),
            "trigonometry": TrigonometrySolver(),
            "statistics":   StatisticsSolver(),
            "matrix":       MatrixSolver(),
            "probability":  ProbabilitySolver(),
        }

    async def dispatch(self, question: str) -> SolveResponse:
        problem_type = MathParser.detect_type(question)

        solver = self.solvers.get(problem_type)

        if solver:
            try:
                response = await asyncio.get_event_loop().run_in_executor(None, solver.solve, question)
                if response.error:
                    # If solver failed, fallback to LLM
                    return await solve_with_llm(question)
                return response
            except Exception as e:
                # Solver crashed, fallback to LLM
                return await solve_with_llm(question)

        # Unknown type → LLM fallback
        return await solve_with_llm(question)
