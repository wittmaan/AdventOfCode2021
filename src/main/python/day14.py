import fileinput
from collections import deque, Counter
from typing import List

# --- Day 14: Extended Polymerization ---
# --- Part one ---

sample_input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".split(
    "\n"
)


def fill(dat):
    instructions = {}
    polymer_template = None
    for line in dat:
        if " -> " in line:
            line_splitted = line.split(" -> ")
            instructions[line_splitted[0]] = line_splitted[1]
        elif line:
            polymer_template = line

    return polymer_template, instructions


def take_pairs(polymer_template):
    pairs = []
    for idx, val in enumerate(polymer_template):
        if idx > 0:
            pairs.append(deque([polymer_template[idx - 1], polymer_template[idx]]))
    return pairs


class Polymerization:
    def __init__(self, dat: List[str], steps: int):
        self.polymer_template, self.instructions = fill(dat)
        self._quantity = None

        if steps > 0:
            self.grow(steps)
        else:
            self.fast_grow()

    def fast_grow(self):
        pairs_count = {
            pair: self.polymer_template.count(pair) for pair in self.instructions
        }
        counter = {
            char: self.polymer_template.count(char)
            for char in self.instructions.values()
        }
        for i in range(40):
            for pair, value in pairs_count.copy().items():
                pairs_count[pair] -= value

                center = self.instructions[pair]
                start = pair[0] + center
                end = center + pair[1]

                pairs_count[start] += value
                pairs_count[end] += value
                counter[center] += value
        self._quantity = max(counter.values()) - min(counter.values())

    def grow(self, steps):
        for step in range(steps):
            self.polymer_template = self.run_one_step(self.polymer_template)
            # print(f"step {step + 1} - polymer_template {self.polymer_template}")

        counter = Counter(self.polymer_template)
        self._quantity = counter.most_common()[0][1] - counter.most_common()[-1][1]

    def run_one_step(self, polymer_template: str):
        pairs = take_pairs(polymer_template)
        return self.insert(pairs)

    def insert(self, pairs):
        for pair in pairs:
            for instruction in self.instructions:
                if "".join(pair) == instruction:
                    pair.insert(1, self.instructions[instruction])
                    break

        result = ""
        for idx, val in enumerate(pairs):
            if idx == 0:
                result += "".join(val)
            else:
                result += "".join(list(val)[1:])
        return result

    def quantity(self):
        return self._quantity


assert Polymerization(sample_input, steps=10).quantity() == 1588

puzzle_input = [_.strip() for _ in fileinput.input()]
solution_part1 = Polymerization(puzzle_input, steps=10).quantity()

assert solution_part1 == 2602
print(f"solution part1: {solution_part1}")

# --- Part two ---

assert Polymerization(sample_input, steps=-1).quantity() == 2188189693529
solution_part2 = Polymerization(puzzle_input, steps=-1).quantity()

assert solution_part2 == 2942885922173
print(f"solution part2: {solution_part2}")
