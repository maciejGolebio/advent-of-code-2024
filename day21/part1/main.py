from functools import cache
from typing import Generator, List, Tuple
from utils import combine_lists, logger
import itertools

Point = Tuple[int, int]

numeric = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]

directional = [[None, "^", "A"], ["<", "v", ">"]]

numeric_start = (2, 3)

directional_start = (2, 0)

example_input = "029A"
example_code = list(example_input)


@cache
def find_char_in_directional(char: str) -> Point:
    for y, row in enumerate(directional):
        for x, cell in enumerate(row):
            if cell == char:
                return x, y


@cache
def is_legal_directional_move(x: int, y: int) -> bool:
    return directional[y][x] is not None


@cache
@logger
def go_directional(
    current: Tuple[int, int], end: Tuple[int, int], current_sequence: str = ""
) -> List[str]:
    if current == end:
        return [current_sequence + "A"]

    if current == (0, 0):
        print(f"Current is 0, 0 number is {directional[0][0]}")
        return None

    x, y = current
    dx, dy = x - end[0], y - end[1]
    paths = []

    if (
        dx > 0
        and is_legal_directional_move(x - 1, y)
        and (value := go_directional((x - 1, y), end, current_sequence + "<"))
        is not None
    ):
        paths.extend(value)
    if (
        dx < 0
        and is_legal_directional_move(x + 1, y)
        and (value := go_directional((x + 1, y), end, current_sequence + ">"))
        is not None
    ):
        paths.extend(value)
    if (
        dy > 0
        and is_legal_directional_move(x, y - 1)
        and (value := go_directional((x, y - 1), end, current_sequence + "^"))
        is not None
    ):
        paths.extend(value)
    if (
        dy < 0
        and is_legal_directional_move(x, y + 1)
        and (value := go_directional((x, y + 1), end, current_sequence + "v"))
        is not None
    ):
        paths.extend(value)

    return paths


@cache
def is_legal_numeric_move(x: int, y: int) -> bool:
    return numeric[y][x] is not None


@cache
def find_char_in_numeric(char: str) -> Point:
    for y, row in enumerate(numeric):
        for x, cell in enumerate(row):
            if cell == char:
                return x, y


@cache
def go_numeric(
    current: Tuple[int, int], end: Tuple[int, int], current_sequence: str = ""
) -> List[str]:
    if current == end:
        return [current_sequence + "A"]

    if current == (0, 3):
        print(f"Current is 0, 3 number is {numeric[3][0]}")
        return None

    x, y = current
    dx, dy = x - end[0], y - end[1]
    paths = []

    if (
        dx > 0
        and is_legal_numeric_move(x - 1, y)
        and (value := go_numeric((x - 1, y), end, current_sequence + "<")) is not None
    ):
        paths.extend(value)
    if (
        dx < 0
        and is_legal_numeric_move(x + 1, y)
        and (value := go_numeric((x + 1, y), end, current_sequence + ">")) is not None
    ):
        paths.extend(value)
    if (
        dy > 0
        and is_legal_numeric_move(x, y - 1)
        and (value := go_numeric((x, y - 1), end, current_sequence + "^")) is not None
    ):
        paths.extend(value)
    if (
        dy < 0
        and is_legal_numeric_move(x, y + 1)
        and (value := go_numeric((x, y + 1), end, current_sequence + "v")) is not None
    ):
        paths.extend(value)

    return paths


def get_numeric_paths(code: List[str]) -> Generator[List[str], str]:
    start = numeric_start
    prev = "A"
    for char in code:
        end = find_char_in_numeric(char)
        yield go_numeric(start, end), char, prev
        start = end
        prev = char


def get_directional_paths_1st_level(
    possible_codes: List[List[str]],
) -> Generator[List[str], str]:
    start = directional_start
    for code in possible_codes:
        paths_for_code = []
        for char in code:
            end = find_char_in_directional(char)
            paths_for_code += [go_directional(start, end)]
            start = end

        # maybe should cut off longer then previous shorter / calc all and continue only with the shortest
        yield combine_lists(paths_for_code), code


def get_directional_paths_2nd_level(
    possible_codes: List[List[str]],
) -> Generator[List[str], str]:
    start = directional_start
    for code in possible_codes:
        # print(f"Code is {code}")
        paths_for_code = []
        for char in code:
            end = find_char_in_directional(char)
            paths_for_code += [go_directional(start, end)]
            start = end

        # maybe
        yield combine_lists(paths_for_code), code

def code_to_numeric(code: List[str]) -> int:
    return int("".join(code).replace("A", ""))

def solve_code(code: List[str]) -> int:
    tmp = float("inf")
    len_third_level_shortest = 0
    for paths, _, _ in get_numeric_paths(code):
        for resp in get_directional_paths_1st_level(paths):
            for resp2 in get_directional_paths_2nd_level(resp[0]):
                for final_path in resp2[0]:
                    if len(final_path) < tmp:
                        tmp = len(final_path)

        len_third_level_shortest += tmp
        tmp = float("inf")

    return len_third_level_shortest * code_to_numeric(code)


if __name__ == "__main__":

    print("\n\n ---------   Final       ---------\n\n")
    result = 0
    codes = [
        "208A",
        "586A",
        "341A",
        "463A",
        "593A",
    ]
    for code in codes:
        result += solve_code(list(code))
    print(f"Result is {result}")
