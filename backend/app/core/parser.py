import re
from typing import Dict, Optional, Any


class MathParser:
    """
    Detects the type of math problem and normalizes input.
    """

    # Trig keywords use word-boundary matching to avoid false matches
    # e.g. "perimeter" contains "sec" as substring — must match whole word only
    PROBLEM_TYPES = {
        "calculus":     ["derivative", "differentiate", "integrate", "integral", "d/dx", "limit"],
        "geometry":     ["area", "perimeter", "volume", "circumference", "surface area", "radius", "circle", "rectangle", "triangle", "square"],
        "statistics":   ["mean", "median", "mode", "standard deviation", "std", "average", "range"],
        "matrix":       ["matrix", "determinant", "transpose", "inverse"],
        "probability":  ["probability", "combination", "permutation", "factorial", "ncr", "npr"],
        "arithmetic":   ["% of", "percent", "bodmas", "evaluate"],
        "algebra":      ["solve", "find x", "equation", "="],
    }

    # Trig keywords checked separately with word boundaries
    TRIG_KEYWORDS = ["sin", "cos", "tan", "sec", "cosec", "csc", "cot", "arcsin", "arccos", "arctan"]

    @staticmethod
    def detect_type(question: str) -> str:
        question_lower = question.lower()

        # Check trig first using word boundaries to avoid substring false matches
        # e.g. "perimeter" contains "sec", "cosec" contains "sec"
        for kw in MathParser.TRIG_KEYWORDS:
            if re.search(rf"\b{kw}\b", question_lower):
                return "trigonometry"

        for problem_type, keywords in MathParser.PROBLEM_TYPES.items():
            if any(keyword in question_lower for keyword in keywords):
                return problem_type

        if "=" in question_lower:
            return "algebra"

        return "unknown"

    @staticmethod
    def normalize(question: str) -> str:
        """
        Normalize input by removing filler words and standardizing format.
        """
        text = question.lower()

        # Remove common filler words — use \s* after to avoid leaving stray letters
        # e.g. "find x if 3x" → remove "find x" and "if" cleanly
        text = re.sub(r"\b(find\s+x|find|solve|what is|calculate|if|the value of|compute)\b\s*", "", text)

        # Remove extra spaces
        text = text.strip()
        text = re.sub(r"\s+", " ", text)

        return text

    @staticmethod
    def extract_equation(question: str) -> Optional[Dict[str, str]]:
        """
        Extract left and right sides of an equation.
        Returns: {"left": "2*x+3", "right": "7"} or None
        """
        normalized = MathParser.normalize(question)

        # Remove spaces for equation parsing
        normalized = normalized.replace(" ", "")

        # Convert implicit multiplication: 2x → 2*x
        normalized = re.sub(r"(\d)([a-z])", r"\1*\2", normalized)

        if "=" in normalized:
            parts = normalized.split("=")
            if len(parts) == 2:
                return {"left": parts[0], "right": parts[1]}

        return None

    @staticmethod
    def extract_geometry_params(question: str) -> Optional[Dict[str, Any]]:
        """
        Extract geometry parameters like radius, length, width, etc.
        """
        question_lower = question.lower()
        params = {}

        # Extract radius
        radius_match = re.search(r"radius\s*(?:is\s*|=\s*)?(\d+\.?\d*)", question_lower)
        if radius_match:
            params["radius"] = float(radius_match.group(1))

        # Extract length
        length_match = re.search(r"length\s*(?:is\s*|=\s*)?(\d+\.?\d*)", question_lower)
        if length_match:
            params["length"] = float(length_match.group(1))

        # Extract width
        width_match = re.search(r"width\s*(?:is\s*|=\s*)?(\d+\.?\d*)", question_lower)
        if width_match:
            params["width"] = float(width_match.group(1))

        # Extract height
        height_match = re.search(r"height\s*(?:is\s*|=\s*)?(\d+\.?\d*)", question_lower)
        if height_match:
            params["height"] = float(height_match.group(1))

        # Detect shape
        if "circle" in question_lower:
            params["shape"] = "circle"
        elif "rectangle" in question_lower:
            params["shape"] = "rectangle"
        elif "triangle" in question_lower:
            params["shape"] = "triangle"
        elif "square" in question_lower:
            params["shape"] = "square"

        return params if params else None
