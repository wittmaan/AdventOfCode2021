import fileinput
from math import prod
from sys import maxsize
from typing import List

# --- Day 9: Smoke Basin ---
# --- Part one ---

sample_input = """2199943210
3987894921
9856789892
8767896789
9899965678""".split(
    "\n"
)


class SmokeBasin:
    def __init__(self, dat: List[str]):
        self.grid = [list(map(int, list(line.strip()))) for line in dat]
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.minimal_points = self.calc_minimal_points()
        self.seen = None

    def calc_minimal_points(self):
        minimal_points = []
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] < min(self.get_neighbours(i, j)):
                    minimal_points.append((i, j))
        return minimal_points

    def get_neighbours(self, i: int, j: int):
        neighbors = [
            (maxsize if i - 1 < 0 else self.grid[i - 1][j]),
            (maxsize if i + 1 >= self.height else self.grid[i + 1][j]),
            (maxsize if j - 1 < 0 else self.grid[i][j - 1]),
            (maxsize if j + 1 >= self.width else self.grid[i][j + 1]),
        ]
        return neighbors

    def sum_risk_levels(self) -> int:
        return sum([self.grid[i][j] + 1 for (i, j) in self.minimal_points])

    def search(self, i: int, j: int):
        if (
            i < 0
            or i >= self.height
            or j < 0
            or j >= self.width
            or self.grid[i][j] == 9
            or (i, j) in self.seen
        ):
            return
        self.seen.add((i, j))
        for delta_x, delta_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            self.search(i + delta_x, j + delta_y)

    def find_basins(self) -> int:
        basins = []
        for minimal_point in self.minimal_points:
            self.seen = set()
            self.search(
                i=minimal_point[0], j=minimal_point[1],
            )
            basins.append(self.seen)

        largest_basins = sorted(basins, key=lambda _: len(_))[-3:]
        return prod([len(_) for _ in largest_basins])


assert SmokeBasin(sample_input).sum_risk_levels() == 15


puzzle_input = [_.strip() for _ in fileinput.input()]
solution_part1 = SmokeBasin(puzzle_input).sum_risk_levels()

assert solution_part1 == 530
print(f"solution part1: {solution_part1}")


# --- Part two ---

assert SmokeBasin(sample_input).find_basins() == 1134

solution_part2 = SmokeBasin(puzzle_input).find_basins()
assert solution_part2 == 1019494
print(f"solution part2: {solution_part2}")
