import fileinput
from typing import List, Tuple, Optional, Any

# --- Day 10: Syntax Scoring ---
# --- Part one ---

sample_input = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".split(
    "\n"
)

OPENING_CHAR = ["(", "{", "<", "["]
CLOSING_CHAR = [")", "}", ">", "]"]

MATCHING_CHAR = [(x, y) for x, y in zip(OPENING_CHAR, CLOSING_CHAR)]

POINT_ERROR_TABLE = {")": 3, "]": 57, "}": 1197, ">": 25137}
POINT_COMPLETION_TABLE = {")": 1, "]": 2, "}": 3, ">": 4}


def get_matching_char(opening_char: str) -> str:
    closing_char = None
    for opening, closing in MATCHING_CHAR:
        if opening_char == opening:
            closing_char = closing
            break
    return closing_char


def is_corrupted(dat: str) -> Tuple[bool, Optional[Any]]:
    corrupted_found = False
    first_illegal_char = None
    for k, v in get_matchings(dat).items():
        needed_closing_char = get_matching_char(k[1])
        if needed_closing_char != v[1]:
            corrupted_found = True
            first_illegal_char = v[1]
            break

    return corrupted_found, first_illegal_char


def get_matchings(dat: str):
    stack = []
    d = {}
    for idx, val in enumerate(dat):
        if val in OPENING_CHAR:
            stack.append((idx, val))
        else:
            if len(stack) > 0:
                d[stack.pop()] = (idx, val)
    return d


assert is_corrupted("(]") == (True, "]")
assert is_corrupted("{()()()>") == (True, ">")
assert is_corrupted("(((()))}") == (True, "}")
assert is_corrupted("<([]){()}[{}])") == (True, ")")
assert is_corrupted("([])") == (False, None)
assert is_corrupted("([])") == (False, None)
assert is_corrupted("<([{}])>") == (False, None)
assert is_corrupted("(((((((((())))))))))") == (False, None)
assert is_corrupted("{([(<{}[<>[]}>{[]{[(<()>") == (True, "}")
assert is_corrupted("[[<[([]))<([[{}[[()]]]") == (True, ")")
assert is_corrupted("[{[{({}]{}}([{[{{{}}([]") == (True, "]")
assert is_corrupted("[<(<(<(<{}))><([]([]()") == (True, ")")
assert is_corrupted("[<(<(<(<{}))><([]([]()") == (True, ")")
assert is_corrupted("<{([([[(<>()){}]>(<<{{") == (True, ">")


def calc_error_score(dat: List[str]) -> int:
    score = 0
    for line in dat:
        corrupted_found, illegal_char = is_corrupted(line)
        if corrupted_found:
            score += POINT_ERROR_TABLE[illegal_char]

    return score


assert calc_error_score(sample_input) == 26397


puzzle_input = [_.strip() for _ in fileinput.input()]
solution_part1 = calc_error_score(puzzle_input)

assert solution_part1 == 392097
print(f"solution part1: {solution_part1}")


# --- Part two ---


def remove_matchings(dat, d):
    result = []
    for idx, val in enumerate(dat):
        if (idx, val) not in d.keys() and (idx, val) not in d.values():
            result.append((idx, val))
    return result


def find_completions(dat: str) -> List[str]:
    new_dat = remove_matchings(dat, get_matchings(dat))

    completions = []
    for (idx, val) in new_dat:
        completions.append(get_matching_char(val))

    completions.reverse()
    return completions


assert find_completions("[({(<(())[]>[[{[]{<()<>>") == [
    "}",
    "}",
    "]",
    "]",
    ")",
    "}",
    ")",
    "]",
]
assert find_completions("<{([{{}}[<[[[<>{}]]]>[]]") == ["]", ")", "}", ">"]


def calc_completion_score(dat: List[str]) -> int:
    scores = []
    for line in dat:
        corrupted_found, _ = is_corrupted(line)
        if not corrupted_found:
            completions = find_completions(line)
            score = 0
            for completion in completions:
                score *= 5
                score += POINT_COMPLETION_TABLE[completion]
            scores.append(score)

    scores.sort()
    return scores[int(len(scores) / 2)]


assert (
    calc_completion_score(
        [
            "[({(<(())[]>[[{[]{<()<>>",
            "[(()[<>])]({[<{<<[]>>(",
            "(((({<>}<{<{<>}{[]{[]{}",
            "{<[[]]>}<{[{[{[]{()[[[]",
            "<{([{{}}[<[[[<>{}]]]>[]]",
        ]
    )
    == 288957
)

solution_part2 = calc_completion_score(puzzle_input)
assert solution_part2 == 4263222782
print(f"solution part2: {solution_part2}")
