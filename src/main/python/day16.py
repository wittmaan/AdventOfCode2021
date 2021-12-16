import fileinput
from collections import deque
from functools import reduce
from operator import mul
from typing import List, Deque

# --- Day 16: Packet Decoder ---
# --- Part one ---

sample_input1 = "D2FE28"
sample_input2 = "38006F45291200"
sample_input3 = "EE00D40C823060"
sample_input4 = "8A004A801A8002F478"

LITERAL_VALUE = 4


def to_binary(dat: str):
    return (bin(int(dat, 16))[2:]).zfill(len(dat) * 4)


def take_elements(dat: Deque, n):
    return [dat.popleft() for _ in range(n)]


def to_int(dat: List[str]) -> int:
    return int(to_str(dat), 2)


def to_str(dat: List[str]) -> str:
    return "".join(dat)


OPERATIONS_LIST = [
    sum,
    lambda x: reduce(mul, x),
    min,
    max,
    None,
    lambda x: int(x[0] > x[1]),
    lambda x: int(x[0] < x[1]),
    lambda x: int(x[0] == x[1]),
]


class PacketDecoder:
    def __init__(self, dat: str):
        self.binary = deque(to_binary(dat))
        self.position = 0
        self.version_sum = 0

    def read(self, n, as_string: bool = False):
        self.position += n
        if as_string:
            return to_str(take_elements(self.binary, n))
        else:
            return to_int(take_elements(self.binary, n))

    def analyze(self):
        self.version_sum += self.read(3)
        type_id = self.read(3)
        if type_id == LITERAL_VALUE:
            read_next = True
            val = ""
            while read_next:
                read_next = bool(self.read(1))
                val += self.read(4, as_string=True)
                if not read_next:
                    return to_int([val])

        values = []
        if self.read(1) == 0:
            subpackets_length = self.read(15)
            limit = self.position + subpackets_length
            while self.position < limit:
                values.append(self.analyze())
        else:
            values = [self.analyze() for _ in range(self.read(11))]
        return OPERATIONS_LIST[type_id](values)


def build_version_sum(dat: str) -> int:
    decoder = PacketDecoder(dat)
    decoder.analyze()
    return decoder.version_sum


assert build_version_sum(sample_input1) == 6
assert build_version_sum(sample_input2) == 9
assert build_version_sum(sample_input3) == 14
assert build_version_sum(sample_input4) == 16

puzzle_input = [_.strip() for _ in fileinput.input()][0]
solution_part1 = build_version_sum(puzzle_input)

assert solution_part1 == 991
print(f"solution part1: {solution_part1}")

# --- Part two ---


def evaluate_expression(dat: str) -> int:
    decoder = PacketDecoder(dat)
    return decoder.analyze()


solution_part2 = evaluate_expression(puzzle_input)

assert solution_part2 == 1264485568252
print(f"solution part2: {solution_part2}")
