import pytest
from app.solvers.algebra import AlgebraSolver
from app.solvers.calculus import CalculusSolver
from app.solvers.geometry import GeometrySolver
from app.solvers.arithmetic import ArithmeticSolver
from app.solvers.trigonometry import TrigonometrySolver


# ── Algebra ──────────────────────────────────────────────────────────────────

class TestAlgebra:
    solver = AlgebraSolver()

    def test_linear(self):
        r = self.solver.solve("2x + 3 = 7")
        assert r.error is None
        assert "2" in r.answer

    def test_linear_negative(self):
        r = self.solver.solve("x - 5 = 10")
        assert "15" in r.answer

    def test_quadratic(self):
        r = self.solver.solve("x^2 - 5x + 6 = 0")
        assert r.error is None
        assert r.answer != ""

    def test_natural_language(self):
        r = self.solver.solve("find x if 3x = 12")
        assert "4" in r.answer

    def test_no_equation(self):
        r = self.solver.solve("just some text")
        assert r.error is not None


# ── Calculus ─────────────────────────────────────────────────────────────────

class TestCalculus:
    solver = CalculusSolver()

    def test_derivative_polynomial(self):
        r = self.solver.solve("derivative of x^2")
        assert r.error is None
        assert "2*x" in r.answer or "2x" in r.answer

    def test_derivative_sum(self):
        r = self.solver.solve("differentiate x^3 + 2x")
        assert r.error is None
        assert r.steps

    def test_integral(self):
        r = self.solver.solve("integrate x^2")
        assert r.error is None
        assert "x**3" in r.answer or "x^3" in r.answer

    def test_unknown_operation(self):
        r = self.solver.solve("limit of x as x approaches 0")
        assert r.error is not None


# ── Geometry ─────────────────────────────────────────────────────────────────

class TestGeometry:
    solver = GeometrySolver()

    def test_circle_area(self):
        r = self.solver.solve("area of circle radius 5")
        assert r.error is None
        assert "78.5" in r.answer

    def test_rectangle_area(self):
        r = self.solver.solve("area of rectangle length 4 width 6")
        assert "24" in r.answer

    def test_triangle_area(self):
        r = self.solver.solve("area of triangle length 6 height 4")
        assert "12" in r.answer

    def test_circle_perimeter(self):
        r = self.solver.solve("perimeter of circle radius 7")
        assert r.error is None
        assert "43.9" in r.answer

    def test_missing_params(self):
        r = self.solver.solve("area of circle")
        assert r.error is not None


# ── Arithmetic ───────────────────────────────────────────────────────────────

class TestArithmetic:
    solver = ArithmeticSolver()

    def test_percentage_of(self):
        r = self.solver.solve("25% of 200")
        assert r.error is None
        assert "50" in r.answer

    def test_what_percent(self):
        r = self.solver.solve("what percent is 30 of 120")
        assert "25" in r.answer

    def test_expression(self):
        r = self.solver.solve("calculate 10 + 5 * 2")
        assert "20" in r.answer

    def test_brackets(self):
        r = self.solver.solve("evaluate (10 + 5) * 2")
        assert "30" in r.answer


# ── Trigonometry ─────────────────────────────────────────────────────────────

class TestTrigonometry:
    solver = TrigonometrySolver()

    def test_sin_30(self):
        r = self.solver.solve("sin 30 degrees")
        assert r.error is None
        assert "1/2" in r.answer

    def test_cos_60(self):
        r = self.solver.solve("cos 60 degrees")
        assert "1/2" in r.answer

    def test_tan_45(self):
        r = self.solver.solve("tan 45 degrees")
        assert "1" in r.answer

    def test_sin_90(self):
        r = self.solver.solve("sin 90 degrees")
        assert "1" in r.answer

    def test_tan_90_undefined(self):
        r = self.solver.solve("tan 90 degrees")
        assert "undefined" in r.answer
