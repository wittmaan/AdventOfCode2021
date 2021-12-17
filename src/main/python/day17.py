from re import findall

# --- Day 17: Trick Shot ---
# --- Part one ---

sample_input = "target area: x=20..30, y=-10..-5"


def build_target_area(dat: str) -> (int, int, int, int):
    x_min, x_max, y_min, y_max = map(int, findall(r"-?\d+", dat))
    return x_min, x_max, y_min, y_max


def run_one_step(
    position: (int, int), velocity: (int, int)
) -> ((int, int), (int, int)):
    new_position = (position[0] + velocity[0], position[1] + velocity[1])

    new_x_velocity = max(0, velocity[0] - 1)
    new_y_velocity = velocity[1] - 1

    return new_position, (new_x_velocity, new_y_velocity)


assert run_one_step(position=(0, 0), velocity=(7, 2)) == ((7, 2), (6, 1))


def calc_best_position(dat: str):
    x_min, x_max, y_min, y_max = build_target_area(dat)

    count = 0
    y_highest = 0
    for delta_x in range(1, x_max + 1):
        for delta_y in range(y_min, -y_max + (y_max - y_min)):
            y_highest_tmp = 0
            position = (0, 0)
            velocity = (delta_x, delta_y)
            while velocity[0] > 0 or position[1] > y_min:
                y_highest_tmp = max(y_highest_tmp, position[1])
                position, velocity = run_one_step(position, velocity)
                if x_min <= position[0] <= x_max and y_min <= position[1] <= y_max:
                    count += 1
                    y_highest = max(y_highest, y_highest_tmp)
                    break

    return y_highest, count


assert calc_best_position(sample_input) == (45, 112)

puzzle_input = "target area: x=128..160, y=-142..-88"
solution_part1, solution_part2 = calc_best_position(puzzle_input)

assert solution_part1 == 10011
print(f"solution part1: {solution_part1}")

# --- Part two ---

assert solution_part2 == 2994
print(f"solution part2: {solution_part2}")
