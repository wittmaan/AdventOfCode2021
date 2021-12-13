import fileinput
from dataclasses import dataclass
from typing import List

# --- Day 13: Transparent Origami ---
# --- Part one ---

sample_input = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".split(
    "\n"
)


@dataclass(unsafe_hash=True)
class Dot:
    x: int
    y: int


@dataclass
class Instruction:
    direction: str
    amount: int


def fill(dat):
    dots = set()
    instructions = []
    for line in dat:
        if "," in line:
            line_splitted = line.split(",")
            dots.add(Dot(int(line_splitted[0]), int(line_splitted[1])))
        if "fold along" in line:
            line_splitted = line[10:].split("=")
            instructions.append(
                Instruction(line_splitted[0].strip(), int(line_splitted[1]))
            )

    return dots, instructions


class Grid:
    def __init__(self, dat: List[str]):
        self.dots, self.instructions = fill(dat)
        self.max_x = max([d.x for d in self.dots])
        self.max_y = max([d.y for d in self.dots])

    def display(self):
        print("\n\n")
        for y in range(self.max_y + 1):
            line = ""
            for x in range(self.max_x + 1):
                if Dot(x, y) in self.dots:
                    line += "#"
                else:
                    line += "."
            print(line)

    def fold(self, times: int):
        num_instructions_done = 0
        for instruction in self.instructions:
            if instruction.direction == "x":
                self.handle_direction_x(instruction)
            elif instruction.direction == "y":
                self.handle_direction_y(instruction)
            else:
                print("unknown direction")

            num_instructions_done += 1

            if num_instructions_done == times:
                break

            print(f"{num_instructions_done} instructions of {len(self.instructions)} done")
            self.display()

    def count_visible_dots(self, times: int):
        self.fold(times=times)
        return len(self.dots)

    def handle_direction_y(self, instruction):
        for x in range(self.max_x + 1):
            for y in range(instruction.amount + 1, self.max_y + 1):
                actual_dot = Dot(x, y)
                if actual_dot in self.dots:
                    self.dots.remove(actual_dot)
                    new_y = instruction.amount - (y - instruction.amount)
                    new_dot = Dot(x, new_y)
                    self.dots.add(new_dot)
        self.max_y = instruction.amount - 1

    def handle_direction_x(self, instruction):
        for x in range(instruction.amount + 1, self.max_x + 1):
            for y in range(self.max_y + 1):
                actual_dot = Dot(x, y)
                if actual_dot in self.dots:
                    self.dots.remove(actual_dot)
                    new_x = instruction.amount - (x - instruction.amount)
                    new_dot = Dot(new_x, y)
                    self.dots.add(new_dot)
        self.max_x = instruction.amount - 1


assert Grid(sample_input).count_visible_dots(times=1) == 17

puzzle_input = [_.strip() for _ in fileinput.input()]
solution_part1 = Grid(puzzle_input).count_visible_dots(times=1)

assert solution_part1 == 942
print(f"solution part1: {solution_part1}")


# --- Part two ---

solution_part2 = Grid(puzzle_input).count_visible_dots(times=100)
# JZGUAPRB