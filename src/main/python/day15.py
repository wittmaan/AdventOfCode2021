import fileinput
from dataclasses import dataclass
from typing import List

# --- Day 15: Chiton ---
# --- Part one ---

sample_input = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".split(
    "\n"
)


@dataclass
class Position:
    i: int
    j: int
    risk: int

    def __lt__(self, other):
        return self.risk < other.risk


class Chiton:
    def __init__(self, dat: List[str], expand: bool = False):
        self.risk_level_map = [
            [Position(i=idx1, j=idx2, risk=int(risk)) for idx2, risk in enumerate(row)]
            for idx1, row in enumerate(dat)
        ]
        self.height = len(self.risk_level_map)
        self.width = len(self.risk_level_map[0])

        if expand:
            self.expand_risk_level_map()

        self._lowest_total_risk = None
        self.calc_risk()

    def expand_risk_level_map(self):
        expanded = [
            [Position(i=i, j=j, risk=0) for i in range(5 * self.height)]
            for j in range(5 * self.width)
        ]
        for x in range(len(expanded)):
            for y in range(len(expanded[0])):
                dist = x // self.height + y // self.width
                newval = self.risk_level_map[x % self.height][y % self.width].risk
                for i in range(dist):
                    newval += 1
                    if newval == 10:
                        newval = 1
                expanded[x][y].risk = newval
        self.risk_level_map = expanded
        self.height = len(self.risk_level_map)
        self.width = len(self.risk_level_map[0])

    def lowest_total_risk(self):
        return self._lowest_total_risk

    def get_deltas(self, position: Position):
        deltas = [
            (position.i + 1, position.j),
            (position.i - 1, position.j),
            (position.i, position.j - 1),
            (position.i, position.j + 1),
        ]
        deltas_tmp = []
        for delta in deltas:
            if delta[0] in range(self.height) and delta[1] in range(self.width):
                deltas_tmp.append(delta)
        return deltas_tmp

    def calc_risk(self):
        self.risk_level_map[0][0].risk = 0
        q = [self.risk_level_map[0][0]]
        risks = {}
        while True:
            current_position = q[0]
            risk = current_position.risk
            if (
                current_position.i == self.height - 1
                and current_position.j == self.width - 1
            ):
                self._lowest_total_risk = risk
                break

            q = q[1:]
            for delta in self.get_deltas(current_position):
                new_risk = risk + self.risk_level_map[delta[0]][delta[1]].risk
                if delta in risks and risks[delta] <= new_risk:
                    continue
                risks[delta] = new_risk
                q.append(Position(i=delta[0], j=delta[1], risk=new_risk))
            q = sorted(q)


assert Chiton(sample_input).lowest_total_risk() == 40

puzzle_input = [_.strip() for _ in fileinput.input()]
solution_part1 = Chiton(puzzle_input).lowest_total_risk()

assert solution_part1 == 487
print(f"solution part1: {solution_part1}")

# --- Part two ---

assert Chiton(sample_input, expand=True).lowest_total_risk() == 315

solution_part2 = Chiton(puzzle_input, expand=True).lowest_total_risk()

assert solution_part2 == 2821
print(f"solution part2: {solution_part2}")
