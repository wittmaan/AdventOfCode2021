import fileinput
from collections import Counter
from dataclasses import dataclass
from typing import List, Optional

# --- Day 5: Hydrothermal Venture ---
# --- Part one ---

sample_input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".split(
    "\n"
)


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Line:
    start: Point
    end: Point
    segment: Optional[List[Point]] = None
    counter: Optional[Counter] = None

    def __post_init__(self):
        self.fill()
        self.count()

    def fill(self):
        self.segment = []
        start_x = min(self.start.x, self.end.x)
        end_x = max(self.start.x, self.end.x)
        start_y = min(self.start.y, self.end.y)
        end_y = max(self.start.y, self.end.y)

        if self.is_horizontal_vertical():
            for x in range(start_x, end_x + 1):
                for y in range(start_y, end_y + 1):
                    self.segment.append(Point(x, y))

        if self.is_diagonal():
            x, y = self.start.x, self.start.y
            while True:
                self.segment.append(Point(x, y))

                if (x, y) == (self.end.x, self.end.y):
                    break

                x = x + 1 if x < self.end.x else x - 1
                y = y + 1 if y < self.end.y else y - 1

    def count(self):
        self.counter = Counter([(_.x, _.y) for _ in self.segment])

    def is_diagonal(self):
        diff_x = abs(self.start.x - self.end.x)
        diff_y = abs(self.start.y - self.end.y)
        return diff_x == diff_y

    def is_horizontal_vertical(self):
        return self.start.x == self.end.x or self.start.y == self.end.y


assert Line(start=Point(1, 1), end=Point(1, 3)).segment == [
    Point(1, 1),
    Point(1, 2),
    Point(1, 3),
]
assert Line(start=Point(9, 7), end=Point(7, 7)).segment == [
    Point(7, 7),
    Point(8, 7),
    Point(9, 7),
]

assert Line(start=Point(9, 7), end=Point(7, 9)).segment == [
    Point(9, 7),
    Point(8, 8),
    Point(7, 9),
]

assert Line(start=Point(6, 4), end=Point(2, 0)).segment == [
    Point(6, 4),
    Point(5, 3),
    Point(4, 2),
    Point(3, 1),
    Point(2, 0),
]

assert Line(start=Point(5, 5), end=Point(8, 2)).segment == [
    Point(5, 5),
    Point(6, 4),
    Point(7, 3),
    Point(8, 2),
]


def count_overlaps(dat: List[Line], num_overlaps=2) -> int:
    counter: Counter = Counter()
    for entry in dat:
        counter += entry.counter

    counter = {_: count for _, count in counter.items() if count >= num_overlaps}
    return len(counter)


assert (
    count_overlaps(
        dat=[
            Line(start=Point(1, 1), end=Point(1, 3)),
            Line(start=Point(1, 2), end=Point(1, 3)),
        ]
    )
    == 2
)


def build_lines(dat: List[str], mode="horizontal_vertical_only") -> List[Line]:
    result = []
    for line in dat:
        start, end = line.split(" -> ")
        x1, y1 = start.split(",")
        x2, y2 = end.split(",")
        result.append(Line(Point(int(x1), int(y1)), Point(int(x2), int(y2))))

    result_filtered = []
    for line in result:
        if line.is_horizontal_vertical():
            result_filtered.append(line)
        elif mode == "diagonal" and line.is_diagonal():
            result_filtered.append(line)

    return result_filtered


sample_input = [_.strip() for _ in sample_input]
assert count_overlaps(build_lines(sample_input, mode="horizontal_vertical_only")) == 5

puzzle_input = [_.strip() for _ in fileinput.input()]
solution_part1 = count_overlaps(build_lines(puzzle_input))

assert solution_part1 == 8350
print(f"solution part1: {solution_part1}")


# --- Part two ---

assert Line(start=Point(1, 1), end=Point(3, 3)).is_diagonal() is True
assert Line(start=Point(1, 1), end=Point(3, 5)).is_diagonal() is False
assert Line(start=Point(9, 7), end=Point(7, 9)).is_diagonal() is True

assert count_overlaps(build_lines(sample_input, mode="diagonal")) == 12

solution_part2 = count_overlaps(build_lines(puzzle_input, mode="diagonal"))
assert solution_part2 == 19374
print(f"solution part2: {solution_part2}")
