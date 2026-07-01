from abc import ABC, abstractmethod
from app.models.schemas import SolveResponse


class BaseSolver(ABC):
    """
    All solvers must implement solve().
    Returns a SolveResponse with steps and answer.
    """

    @abstractmethod
    def solve(self, question: str) -> SolveResponse:
        pass
