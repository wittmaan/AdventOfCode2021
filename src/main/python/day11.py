import fileinput
from typing import List

# --- Day 11: Dumbo Octopus ---
# --- Part one ---

sample_input = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".split(
    "\n"
)


def neighbours(idx_i: int, idx_j: int, height: int, width: int):
    for i in range(idx_i - 1, idx_i + 2):
        for j in range(idx_j - 1, idx_j + 2):
            if 0 <= i < height and 0 <= j < width and (i, j) != (idx_i, idx_j):
                yield i, j


class Octopus:
    def __init__(self, energy_level: int):
        self.energy_level = energy_level
        self.is_flashed = False


class DumboOctopusSimulator:
    def __init__(self, dat: List[str], steps: int):
        self.octopuses = [[Octopus(int(_)) for _ in line] for line in dat]
        self.height = len(self.octopuses)
        self.width = len(self.octopuses[0])
        self.all_flashed = True
        self.steps_all_flashed = steps
        self.flashes = 0

        while steps:
            self.run_one_step()

            if self.all_flashed:
                self.steps_all_flashed -= steps - 1
                break

            steps -= 1

    def run_one_step(self):
        for i in range(self.height):
            for j in range(self.width):
                self.octopuses[i][j].energy_level += 1

        self.update()
        self.count_flashes()

    def update(self):
        flashed = True
        while flashed:
            flashed = False
            for i in range(self.height):
                for j in range(self.width):
                    if (
                        self.octopuses[i][j].energy_level > 9
                        and not self.octopuses[i][j].is_flashed
                    ):
                        flashed = True
                        self.octopuses[i][j].is_flashed = flashed
                        for idx_i, idx_j in neighbours(
                            idx_i=i, idx_j=j, height=self.height, width=self.width
                        ):
                            self.octopuses[idx_i][idx_j].energy_level += 1

    def count_flashes(self):
        self.all_flashed = True
        for i in range(self.height):
            for j in range(self.width):
                if self.octopuses[i][j].is_flashed:
                    self.flashes += 1
                    self.octopuses[i][j].energy_level = 0
                    self.octopuses[i][j].is_flashed = False
                else:
                    self.all_flashed = False


assert DumboOctopusSimulator(sample_input, steps=100).flashes == 1656


puzzle_input = [_.strip() for _ in fileinput.input()]
solution_part1 = DumboOctopusSimulator(puzzle_input, steps=100).flashes

assert solution_part1 == 1601
print(f"solution part1: {solution_part1}")


# --- Part two ---

assert DumboOctopusSimulator(sample_input, steps=200).steps_all_flashed == 195

solution_part2 = DumboOctopusSimulator(puzzle_input, steps=500).steps_all_flashed
assert solution_part2 == 368
print(f"solution part2: {solution_part2}")
