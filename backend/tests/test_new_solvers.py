import pytest
from app.solvers.statistics import StatisticsSolver
from app.solvers.matrix import MatrixSolver
from app.solvers.probability import ProbabilitySolver


# ── Statistics ───────────────────────────────────────────────────────────────

class TestStatistics:
    solver = StatisticsSolver()

    def test_mean(self):
        r = self.solver.solve("mean of 2, 4, 6, 8, 10")
        assert r.error is None
        assert "6" in r.answer

    def test_median_odd(self):
        r = self.solver.solve("median of 3, 1, 4, 1, 5")
        assert "3" in r.answer

    def test_median_even(self):
        r = self.solver.solve("median of 1, 2, 3, 4")
        assert "2.5" in r.answer

    def test_mode(self):
        r = self.solver.solve("mode of 1, 2, 2, 3, 3, 3")
        assert "3" in r.answer

    def test_stdev(self):
        r = self.solver.solve("standard deviation of 2, 4, 4, 4, 5, 5, 7, 9")
        assert r.error is None
        assert r.answer != ""

    def test_range(self):
        r = self.solver.solve("range of 5, 10, 15, 20")
        assert "15" in r.answer

    def test_no_numbers(self):
        r = self.solver.solve("mean of nothing")
        assert r.error is not None

    def test_unknown_operation(self):
        r = self.solver.solve("variance of 1, 2, 3")
        assert r.error is not None


# ── Matrix ───────────────────────────────────────────────────────────────────

class TestMatrix:
    solver = MatrixSolver()

    def test_determinant_2x2(self):
        r = self.solver.solve("determinant of [[1,2],[3,4]]")
        assert r.error is None
        assert "-2" in r.answer

    def test_transpose(self):
        r = self.solver.solve("transpose [[1,2],[3,4]]")
        assert r.error is None
        assert "1" in r.answer

    def test_inverse(self):
        r = self.solver.solve("inverse of [[1,2],[3,4]]")
        assert r.error is None
        assert r.answer != ""

    def test_singular_matrix(self):
        r = self.solver.solve("inverse of [[1,2],[2,4]]")
        assert r.error is not None

    def test_multiply(self):
        r = self.solver.solve("multiply [[1,2],[3,4]] [[5,6],[7,8]]")
        assert r.error is None
        assert "19" in r.answer

    def test_add(self):
        r = self.solver.solve("add [[1,2],[3,4]] [[5,6],[7,8]]")
        assert r.error is None
        assert "6" in r.answer

    def test_no_matrix(self):
        r = self.solver.solve("determinant of something")
        assert r.error is not None


# ── Probability ──────────────────────────────────────────────────────────────

class TestProbability:
    solver = ProbabilitySolver()

    def test_combination(self):
        r = self.solver.solve("combination 5 3")
        assert r.error is None
        assert "10" in r.answer

    def test_permutation(self):
        r = self.solver.solve("permutation 5 3")
        assert r.error is None
        assert "60" in r.answer

    def test_probability_out_of(self):
        r = self.solver.solve("probability 3 out of 10")
        assert r.error is None
        assert "0.3" in r.answer

    def test_factorial(self):
        r = self.solver.solve("5!")
        assert r.error is None
        assert "120" in r.answer

    def test_factorial_word(self):
        r = self.solver.solve("factorial of 6")
        assert "720" in r.answer

    def test_r_greater_than_n(self):
        r = self.solver.solve("combination 3 5")
        assert r.error is not None
