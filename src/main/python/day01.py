import fileinput
from collections import deque
from typing import List

import numpy as np

# --- Day 1: Sonar Sweep ---
# --- Part one ---

sample_input = """199
200
208
210
200
207
240
269
260
263""".split(
    "\n"
)


def count_increases(dat: List[int]) -> int:
    consecutive_diffs = np.diff(dat)
    return sum(consecutive_diffs > 0)


sample_input = [int(_) for _ in sample_input]
assert count_increases(sample_input) == 7

puzzle_input = [int(_.strip()) for _ in fileinput.input()]
solution_part1 = count_increases(puzzle_input)

assert solution_part1 == 1462
print(f"solution part1: {solution_part1}")


# --- Part two ---


def count_increases_extended(dat: List[int], window_size=3) -> int:
    buffer = deque(maxlen=window_size)
    sum_list = []
    for d in dat:
        buffer.append(d)
        if len(buffer) == window_size:
            sum_list.append(sum(buffer))

    return count_increases(sum_list)


assert count_increases_extended(sample_input) == 5

solution_part2 = count_increases_extended(puzzle_input)
assert solution_part2 == 1497
print(f"solution part2: {solution_part2}")
