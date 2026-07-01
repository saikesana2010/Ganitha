import pytest
from app.core.parser import MathParser


class TestDetectType:
    def test_algebra(self):
        assert MathParser.detect_type("2x + 3 = 7") == "algebra"

    def test_calculus_derivative(self):
        assert MathParser.detect_type("derivative of x^2") == "calculus"

    def test_calculus_integral(self):
        assert MathParser.detect_type("integrate x^2") == "calculus"

    def test_geometry_area(self):
        assert MathParser.detect_type("area of circle radius 5") == "geometry"

    def test_geometry_perimeter(self):
        assert MathParser.detect_type("perimeter of rectangle") == "geometry"

    def test_trigonometry(self):
        assert MathParser.detect_type("sin 30 degrees") == "trigonometry"

    def test_arithmetic_percent(self):
        assert MathParser.detect_type("25% of 200") == "arithmetic"

    def test_unknown(self):
        assert MathParser.detect_type("hello world") == "unknown"


class TestExtractEquation:
    def test_simple(self):
        result = MathParser.extract_equation("2x + 3 = 7")
        assert result is not None
        assert result["left"] == "2*x+3"
        assert result["right"] == "7"

    def test_natural_language(self):
        result = MathParser.extract_equation("find x if 3x = 12")
        assert result is not None
        assert "3*x" in result["left"]

    def test_no_equation(self):
        result = MathParser.extract_equation("area of circle")
        assert result is None


class TestExtractGeometryParams:
    def test_circle(self):
        params = MathParser.extract_geometry_params("area of circle radius 5")
        assert params["shape"] == "circle"
        assert params["radius"] == 5.0

    def test_rectangle(self):
        params = MathParser.extract_geometry_params("area of rectangle length 4 width 6")
        assert params["shape"] == "rectangle"
        assert params["length"] == 4.0
        assert params["width"] == 6.0

    def test_no_params(self):
        params = MathParser.extract_geometry_params("hello world")
        assert params is None
