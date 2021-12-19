import fileinput
from itertools import permutations
from typing import List


# --- Day 18: Snailfish ---
# --- Part one ---


def build(dat: List[str]):
    return [eval(line) for line in dat]


assert build(["[1,2]"]) == [[1, 2]]
assert build(["[[1,2],3]"]) == [[[1, 2], 3]]


def magnitude(dat):
    if type(dat) == int:
        return dat
    left, right = dat
    return 3 * magnitude(left) + 2 * magnitude(right)


class SnailfishCalculator:
    def __init__(self, current):
        self.current = current

    def add(self, other):
        result = [self.current, other]
        while True:
            is_exploded, result, _, _ = self.explode(dat=result, depth=0)
            if not is_exploded:
                previous = result
                result = self.split(result)
                if result == previous:
                    self.current = result
                    break

    def explode(self, dat, depth):
        if type(dat) == int:
            return False, dat, 0, 0
        left, right = dat

        if depth == 4:
            return True, 0, left, right

        is_exploded, next_dat, next_left, next_right = self.explode(left, depth + 1)
        if is_exploded:
            return True, [next_dat, self.add_left(right, next_right)], next_left, 0

        is_exploded, next_dat, next_left, next_right = self.explode(right, depth + 1)
        if is_exploded:
            return True, [self.add_right(left, next_left), next_dat], 0, next_right

        return False, dat, 0, 0

    def add_left(self, left, right):
        if not right:
            return left
        if type(left) == int:
            return left + right
        return [self.add_left(left[0], right), left[1]]

    def add_right(self, left, right):
        if not right:
            return left
        if type(left) == int:
            return left + right
        return [left[0], self.add_right(left[1], right)]

    def split(self, dat):
        if type(dat) == int:
            if dat > 9:
                return [dat // 2, dat // 2 + (dat & 1)]
            return dat
        next_left, next_right = dat
        left = self.split(next_left)
        if left != next_left:
            return [left, next_right]
        return [next_left, self.split(next_right)]


snailfish = SnailfishCalculator(build(["[1,2]"])[0])
snailfish.add(build(["[[3,4],5]"])[0])
assert snailfish.current == [[1, 2], [[3, 4], 5]]


puzzle_input = build([_.strip() for _ in fileinput.input()])


def calc_magnitude(dat):
    snailfish = SnailfishCalculator(dat[0])
    for next_snailfish in dat[1:]:
        snailfish.add(next_snailfish)
    return magnitude(snailfish.current)


solution_part1 = calc_magnitude(puzzle_input)

assert solution_part1 == 4111
print(f"solution part1: {solution_part1}")

# --- Part two ---


def calc_max_magnitude(dat):
    max_magnitude = 0
    for a, b in permutations(dat, 2):
        snailfish = SnailfishCalculator(a)
        snailfish.add(b)
        max_magnitude = max(max_magnitude, magnitude(snailfish.current))
    return max_magnitude


solution_part2 = calc_max_magnitude(puzzle_input)

assert solution_part2 == 4917
print(f"solution part2: {solution_part2}")
