import fileinput
from typing import List

# --- Day 8: Seven Segment Search ---
# --- Part one ---

sample_input = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"

NEEDED_SEGMENT_COUNTS = (2, 3, 4, 7)  # corresponding to 1, 7, 4 and 8


def count_digits(dat: List[str]) -> int:
    count = 0
    for line in dat:
        signal_pattern, output_value = line.split("|")
        output_value_splitted = output_value.strip().split(" ")
        for o in output_value_splitted:
            if len(o) in NEEDED_SEGMENT_COUNTS:
                count += 1
    return count


assert count_digits([sample_input]) == 0

sample_input2 = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

assert count_digits(sample_input2.split("\n")) == 26

puzzle_input = [_.strip() for _ in fileinput.input()]
solution_part1 = count_digits(puzzle_input)

assert solution_part1 == 255
print(f"solution part1: {solution_part1}")


# --- Part two ---


def count_digits_with_mapping(dat: List[str]) -> int:
    count = 0
    for line in dat:
        signal_pattern, output_value = line.split("|")
        output_value_splitted = output_value.strip().split(" ")
        signal_pattern_splitted = signal_pattern.strip().split(" ")

        code = {}
        for s in signal_pattern_splitted:
            if len(s) == 2:
                code[1] = set(s)
            elif len(s) == 3:
                code[7] = set(s)
            elif len(s) == 4:
                code[4] = set(s)
            elif len(s) == 7:
                code[8] = set(s)

        for s in signal_pattern_splitted:
            if len(s) == 6:
                if len(code[4].intersection(s)) == 4:
                    code[9] = set(s)
                elif len(code[7].intersection(s)) == 3:
                    code[0] = set(s)
                else:
                    code[6] = set(s)
            elif len(s) == 5:
                if len(code[7].intersection(s)) == 3:
                    code[3] = set(s)
                elif len(code[4].intersection(s)) == 3:
                    code[5] = set(s)
                else:
                    code[2] = set(s)

        result = ""
        for o in output_value_splitted:
            for c in code:
                if sorted(code[c]) == sorted(o):
                    result += str(c)
                    break

        count += int(result)

    return count


assert count_digits_with_mapping([sample_input]) == 5353

solution_part2 = count_digits_with_mapping(puzzle_input)
assert solution_part2 == 982158
print(f"solution part2: {solution_part2}")
