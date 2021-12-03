import fileinput
from collections import Counter, defaultdict
from typing import List, DefaultDict

# --- Day 3: Binary Diagnostic ---
# --- Part one ---

sample_input = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".split(
    "\n"
)


def count_numbers(dat: List[str]) -> DefaultDict[int, Counter]:
    result = defaultdict(Counter)
    for line in dat:
        tmp = [Counter(_) for _ in line]
        for idx, val in enumerate(tmp):
            result[idx] += Counter(val)
    return result


def calc_gamma_rate(dat: DefaultDict[int, Counter]) -> str:
    return "".join([_[1].most_common(1)[0][0] for _ in dat.items()])


def calc_epsilon_rate(dat: DefaultDict[int, Counter]) -> str:
    return "".join([_[1].most_common()[-1][0] for _ in dat.items()])


def calc_power_consumption(dat: List[str]) -> int:
    counter = count_numbers(dat)
    gamma_rate = calc_gamma_rate(counter)
    epsilon_rate = calc_epsilon_rate(counter)
    return int(gamma_rate, 2) * int(epsilon_rate, 2)


assert calc_power_consumption(sample_input) == 198

puzzle_input = [_.strip() for _ in fileinput.input()]
solution_part1 = calc_power_consumption(puzzle_input)

assert solution_part1 == 1071734
print(f"solution part1: {solution_part1}")


# --- Part two ---


def filter_lines(dat, pos, mode: str):
    counter = count_numbers(dat)
    result = []

    number_to_check = ""
    most_common_pair = counter[pos].most_common(2)

    if mode == "oxygen_generator":
        if (
            len(most_common_pair) == 1
            or most_common_pair[0][1] != most_common_pair[1][1]
        ):
            number_to_check = most_common_pair[0][0]
        else:
            number_to_check = "1"
    elif mode == "co2_scrubber":
        if (
            len(most_common_pair) == 1
            or most_common_pair[0][1] != most_common_pair[1][1]
        ):
            number_to_check = most_common_pair[1][0]
        else:
            number_to_check = "0"

    for line in dat:
        if number_to_check == line[pos]:
            result.append(line)
    return result


def calc_rating(dat: List[str], mode: str = "oxygen_generator") -> int:
    max_position = len(dat[0])
    pos = 0
    actual_dat = dat

    while True:
        actual_dat = filter_lines(dat=actual_dat, pos=pos, mode=mode)
        pos += 1

        if len(actual_dat) == 1 or pos > max_position:
            break

    return int(actual_dat[0], 2)


assert calc_rating(sample_input, mode="oxygen_generator") == 23
assert calc_rating(sample_input, mode="co2_scrubber") == 10


def calc_life_support_rating(dat: List[str]) -> int:
    oxygen_generator_rating = calc_rating(dat, mode="oxygen_generator")
    co2_scrubber_rating = calc_rating(dat, mode="co2_scrubber")
    return oxygen_generator_rating * co2_scrubber_rating


assert calc_life_support_rating(sample_input) == 230

solution_part2 = calc_life_support_rating(puzzle_input)
assert solution_part2 == 6124992
print(f"solution part2: {solution_part2}")
