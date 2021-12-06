import fileinput
from collections import Counter

# --- Day 6: Lanternfish ---
# --- Part one ---


sample_input = "3,4,3,1,2"


def simulate(dat: str, day_limit: int):
    result = Counter([int(_) for _ in dat.split(",")])

    day = 1
    while True:
        # print(f"result = {result}")
        result_new = Counter()
        for laternfish, value in result.items():
            if laternfish == 0:
                result_new[6] += value
                result_new[8] += value
            else:
                result_new[laternfish - 1] += value

        result = result_new

        day += 1
        if day == (day_limit + 1):
            break

    return sum(result.values())


assert simulate(sample_input, day_limit=18) == 26
assert simulate(sample_input, day_limit=80) == 5934

puzzle_input = [_.strip() for _ in fileinput.input()][0]
solution_part1 = simulate(puzzle_input, day_limit=80)

assert solution_part1 == 365862
print(f"solution part1: {solution_part1}")


# --- Part two ---

solution_part2 = simulate(puzzle_input, day_limit=256)
assert solution_part2 == 1653250886439
print(f"solution part2: {solution_part2}")
