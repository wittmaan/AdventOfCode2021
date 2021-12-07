import fileinput

# --- Day 7: The Treachery of Whales ---
# --- Part one ---

sample_input = "16,1,2,0,4,2,7,1,2,14"


def calc_minimal_fuel(dat: str, constant_rate: bool = True):
    initial_positions = [int(_) for _ in dat.split(",")]

    if constant_rate:
        fuels = []
        for position1 in initial_positions:
            fuel = 0
            for position2 in initial_positions:
                fuel += abs(position1 - position2)
            fuels.append(fuel)
        minimal_fuel = min(fuels)
    else:
        minimal_fuel = 1.0e08
        for position1 in range(min(initial_positions), max(initial_positions)):
            result = [
                ((diff * (diff + 1)) / 2)
                for diff in (
                    abs(position1 - position2) for position2 in initial_positions
                )
            ]
            minimal_fuel = min(minimal_fuel, sum(result))

    return int(minimal_fuel)


assert calc_minimal_fuel(sample_input) == 37

puzzle_input = [_.strip() for _ in fileinput.input()][0]
solution_part1 = calc_minimal_fuel(puzzle_input)

assert solution_part1 == 336120
print(f"solution part1: {solution_part1}")


# --- Part two ---

assert calc_minimal_fuel(sample_input, constant_rate=False) == 168

solution_part2 = solution_part1 = calc_minimal_fuel(puzzle_input, constant_rate=False)
assert solution_part2 == 96864235
print(f"solution part2: {solution_part2}")
