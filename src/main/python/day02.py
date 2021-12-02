import fileinput
from dataclasses import dataclass
from typing import List


# --- Day 2: Dive! ---
# --- Part one ---

sample_input = """forward 5
down 5
forward 8
up 3
down 8
forward 2""".split(
    "\n"
)


@dataclass
class Position:
    horizontal: int
    depth: int


def calc_position(dat: List[str], use_aim: bool = False) -> Position:
    position = Position(0, 0)
    aim = 0
    for d in dat:
        instruction, value = d.split()
        if instruction == "forward":
            position.horizontal += int(value)
            if use_aim:
                position.depth += int(value) * aim
        elif instruction == "down":
            if use_aim:
                aim += int(value)
            else:
                position.depth += int(value)
        elif instruction == "up":
            if use_aim:
                aim -= int(value)
            else:
                position.depth -= int(value)

    return position


def get_position_value(dat: List[str], use_aim: bool = False) -> int:
    position = calc_position(dat, use_aim)
    return position.horizontal * position.depth


assert get_position_value(sample_input) == 150

puzzle_input = [_.strip() for _ in fileinput.input()]
solution_part1 = get_position_value(puzzle_input)

assert solution_part1 == 1690020
print(f"solution part1: {solution_part1}")


# --- Part two ---

assert get_position_value(sample_input, use_aim=True) == 900
solution_part2 = get_position_value(puzzle_input, use_aim=True)

assert solution_part2 == 1408487760
print(f"solution part2: {solution_part2}")
