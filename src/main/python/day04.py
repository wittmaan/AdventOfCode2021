import fileinput
from typing import List

import numpy as np

# --- Day 4: Giant Squid ---
# --- Part one ---

sample_input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7""".split(
    "\n"
)


class BoardChecker:
    def __init__(self, dat: List[List[int]]):
        self.dat = dat
        self.winner_idx = None
        self.sum_unmarked_numbers = 0
        self.indicator = np.zeros(np.shape(dat)).tolist()
        self.length_all_matched = len(dat)

    def run(self, number: int):
        # print(f"checking number {number}")
        is_winner = False

        for idx1, val1 in enumerate(self.dat):
            for idx2, val2 in enumerate(val1):
                if number == val2:
                    self.indicator[idx1][idx2] = 1.0

            if sum(self.indicator[idx1]) == self.length_all_matched:
                is_winner = True
                self.winner_idx = idx1
                self.sum_unmarked_numbers = self.calc_sum_unmarked_numbers()
                break

        return is_winner

    def calc_sum_unmarked_numbers(self):
        sum_unmarked_numbers = 0
        for idx1, val1 in enumerate(self.dat):
            for idx2, val2 in enumerate(val1):
                if self.indicator[idx1][idx2] == 0.0:
                    sum_unmarked_numbers += self.dat[idx1][idx2]
        return sum_unmarked_numbers


class Board:
    def __init__(self, dat: List[str]):
        self.checker_rows = None
        self.checker_cols = None
        self.fill(dat)
        self.is_winner = None

    def fill(self, dat):
        matrix_rows = []
        for line in dat:
            matrix_rows.append([int(_) for _ in line.split()])
        matrix_cols = list(map(list, zip(*matrix_rows)))

        self.checker_rows = BoardChecker(matrix_rows)
        self.checker_cols = BoardChecker(matrix_cols)

    def check(self, number_to_check: int):
        if self.checker_rows.run(number_to_check):
            self.is_winner = True
            return self.checker_rows
        elif self.checker_cols.run(number_to_check):
            self.is_winner = True
            return self.checker_cols


class BingoSubsystem:
    def __init__(self, dat: List[str]):
        self.numbers = None
        self.boards = []
        self.fill(dat)

    def fill(self, dat):
        numbers_done = False
        board_buffer = []

        for line in dat:
            if line != "":
                if not numbers_done:
                    self.numbers = [int(_) for _ in line.split(",")]
                    numbers_done = True
                else:
                    board_buffer.append(line)
                    if len(board_buffer) == 5:
                        self.boards.append(Board(board_buffer))
                        board_buffer = []

    def check_first_winner(self):
        winner_found = False
        while True:
            number_to_check = self.numbers[:1][0]
            self.numbers = self.numbers[1:]
            for board in self.boards:
                checker: BoardChecker = board.check(number_to_check)

                if checker is not None and checker.winner_idx is not None:
                    winner_found = True
                    break

            if not self.numbers or winner_found:
                break

        return number_to_check * checker.sum_unmarked_numbers

    def check_last_winner(self):
        while True:
            number_to_check = self.numbers[:1][0]
            self.numbers = self.numbers[1:]

            for board in self.boards:
                checker: BoardChecker = board.check(number_to_check)

            self.boards = [_ for _ in self.boards if not _.is_winner]

            if not self.numbers or len(self.boards) == 0:
                break

        return number_to_check * checker.sum_unmarked_numbers


assert BingoSubsystem(sample_input).check_first_winner() == 4512


puzzle_input = [_.strip() for _ in fileinput.input()]
solution_part1 = BingoSubsystem(puzzle_input).check_first_winner()

assert solution_part1 == 51034
print(f"solution part1: {solution_part1}")


# --- Part two ---


assert BingoSubsystem(sample_input).check_last_winner() == 1924

solution_part2 = BingoSubsystem(puzzle_input).check_last_winner()
assert solution_part2 == 5434
print(f"solution part2: {solution_part2}")
