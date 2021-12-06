import fileinput
from collections import deque
from typing import List

import numpy as np

# --- Day 6: Lanternfish ---
# --- Part one ---


sample_input = "3,4,3,1,2"


class Laternfish:
    def __init__(self, timer: int = 9):
        self.timer = timer

    def update(self):
        self.timer = self.timer - 1 if self.timer > 0 else 6

    def __repr__(self):
        return f"timer = {self.timer}"


def simulate(dat: str, day_limit: int):
    laternfish_list = [Laternfish(int(_)) for _ in dat.split(",")]
    # print(f"initial state {laternfish_list}")

    day = 1
    while True:
        [_.update() for _ in laternfish_list]
        num_zero_timer = sum([_.timer == 0 for _ in laternfish_list])
        # print(f"day = {day} {laternfish_list} {num_zero_timer}")
        print(day)

        day += 1

        if day == (day_limit + 1):
            break

        [laternfish_list.append(Laternfish()) for _ in range(num_zero_timer)]

    return len(laternfish_list)


assert simulate(sample_input, day_limit=18) == 26
assert simulate(sample_input, day_limit=80) == 5934

# puzzle_input = [_.strip() for _ in fileinput.input()][0]
# solution_part1 = simulate(puzzle_input, day_limit=80)
#
# assert solution_part1 == 365862
# print(f"solution part1: {solution_part1}")


# --- Part two ---

# solution_part2 = simulate(puzzle_input, day_limit=256)
# assert solution_part2 == 1497
# print(f"solution part2: {solution_part2}")
