import re
import math
from statistics import mean, median, mode, stdev, multimode
from app.solvers.base import BaseSolver
from app.models.schemas import SolveResponse


class StatisticsSolver(BaseSolver):

    def solve(self, question: str) -> SolveResponse:
        numbers = self._extract_numbers(question)
        if not numbers:
            return SolveResponse(
                type="statistics", question=question, steps=[], answer="",
                error="Could not extract a list of numbers from the question"
            )

        q = question.lower()
        if "mean" in q or "average" in q:
            return self._mean(question, numbers)
        if "median" in q:
            return self._median(question, numbers)
        if "mode" in q:
            return self._mode(question, numbers)
        if "standard deviation" in q or "std" in q:
            return self._stdev(question, numbers)
        if "range" in q:
            return self._range(question, numbers)

        return SolveResponse(
            type="statistics", question=question, steps=[], answer="",
            error="Specify operation: mean, median, mode, standard deviation, or range"
        )

    # ------------------------------------------------------------------ #

    def _mean(self, question, nums):
        result = mean(nums)
        steps = [
            f"Given numbers: {nums}",
            f"Mean = sum of all values ÷ count",
            f"Sum = {sum(nums)}",
            f"Count = {len(nums)}",
            f"Mean = {sum(nums)} ÷ {len(nums)} = {result}"
        ]
        return SolveResponse(type="statistics", question=question, steps=steps, answer=str(result))

    def _median(self, question, nums):
        sorted_nums = sorted(nums)
        n = len(sorted_nums)
        result = median(nums)
        steps = [
            f"Given numbers: {nums}",
            f"Sorted: {sorted_nums}",
            f"Count = {n}",
        ]
        if n % 2 == 1:
            mid = n // 2
            steps.append(f"Odd count → middle value at index {mid}: {sorted_nums[mid]}")
        else:
            m1, m2 = sorted_nums[n // 2 - 1], sorted_nums[n // 2]
            steps.append(f"Even count → average of middle two: ({m1} + {m2}) / 2 = {result}")
        steps.append(f"Median = {result}")
        return SolveResponse(type="statistics", question=question, steps=steps, answer=str(result))

    def _mode(self, question, nums):
        modes = multimode(nums)
        steps = [
            f"Given numbers: {nums}",
            "Count frequency of each value:",
        ]
        freq = {}
        for n in nums:
            freq[n] = freq.get(n, 0) + 1
        for val, count in sorted(freq.items()):
            steps.append(f"  {val} → {count} time(s)")
        steps.append(f"Mode (most frequent) = {modes}")
        return SolveResponse(type="statistics", question=question, steps=steps, answer=str(modes))

    def _stdev(self, question, nums):
        if len(nums) < 2:
            return SolveResponse(
                type="statistics", question=question, steps=[], answer="",
                error="Need at least 2 numbers for standard deviation"
            )
        avg = mean(nums)
        variance = sum((x - avg) ** 2 for x in nums) / (len(nums) - 1)
        result = math.sqrt(variance)
        steps = [
            f"Given numbers: {nums}",
            f"Mean = {avg}",
            f"Squared deviations: {[round((x - avg)**2, 4) for x in nums]}",
            f"Variance = sum of squared deviations / (n-1) = {round(variance, 6)}",
            f"Standard Deviation = √{round(variance, 6)} = {round(result, 6)}"
        ]
        return SolveResponse(type="statistics", question=question, steps=steps, answer=str(round(result, 6)))

    def _range(self, question, nums):
        result = max(nums) - min(nums)
        steps = [
            f"Given numbers: {nums}",
            f"Max = {max(nums)}, Min = {min(nums)}",
            f"Range = Max - Min = {max(nums)} - {min(nums)} = {result}"
        ]
        return SolveResponse(type="statistics", question=question, steps=steps, answer=str(result))

    def _extract_numbers(self, question: str):
        return [float(n) for n in re.findall(r'-?\d+\.?\d*', question)]
