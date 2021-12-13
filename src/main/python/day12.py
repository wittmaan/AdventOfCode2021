import fileinput
from collections import defaultdict
from typing import List

# --- Day 12: Passage Pathing ---
# --- Part one ---

sample_input = """start-A
start-b
A-c
A-b
b-d
A-end
b-end""".split(
    "\n"
)


sample_input2 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".split(
    "\n"
)


START = "start"
END = "end"


def get_possible_movements(dat: List[str]):
    cave_system = []
    for line in dat:
        cave_system.append(line.strip().split("-"))

    possible_movements = {}
    for cave_a, cave_b in cave_system:
        possible_movements[cave_a] = set()
        possible_movements[cave_b] = set()

    for cave_a, cave_b in cave_system:
        if cave_a != START:
            possible_movements[cave_b].add(cave_a)
        if cave_b != START:
            possible_movements[cave_a].add(cave_b)

    return possible_movements


def count_paths(cave: str, visited, possible_movements) -> int:
    if cave in visited:
        return False
    if cave == END:
        return True
    if cave.islower():
        visited.add(cave)

    counts = sum(
        [
            count_paths(neighbor, visited, possible_movements)
            for neighbor in possible_movements[cave]
        ]
    )
    visited.discard(cave)

    return counts


assert count_paths(START, set(), get_possible_movements(sample_input)) == 10
assert count_paths(START, set(), get_possible_movements(sample_input2)) == 226


puzzle_input = [_.strip() for _ in fileinput.input()]
solution_part1 = count_paths(START, set(), get_possible_movements(puzzle_input))

assert solution_part1 == 3450
print(f"solution part1: {solution_part1}")


# --- Part two ---


def count_paths_extended(
    cave: str, visited, possible_movements, is_visited_twice
) -> int:
    if visited[cave] > 0 and is_visited_twice:
        return False
    if cave == END:
        return True
    if cave.islower():
        visited[cave] += 1
        if visited[cave] == 2:
            is_visited_twice = not is_visited_twice

    counts = sum(
        [
            count_paths_extended(
                neighbor, visited, possible_movements, is_visited_twice
            )
            for neighbor in possible_movements[cave]
            if neighbor != START
        ]
    )
    visited[cave] -= 1

    return counts


assert (
    count_paths_extended(
        START, defaultdict(int), get_possible_movements(sample_input), False
    )
    == 36
)

assert (
    count_paths_extended(
        START, defaultdict(int), get_possible_movements(sample_input2), False
    )
    == 3509
)

solution_part2 = count_paths_extended(
    START, defaultdict(int), get_possible_movements(puzzle_input), False
)

assert solution_part2 == 96528
print(f"solution part2: {solution_part2}")
