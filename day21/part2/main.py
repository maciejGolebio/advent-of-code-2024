from functools import cache
from itertools import product
from typing import Generator, List, Tuple
from utils import logger

Point = Tuple[int, int]

numeric = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]
directional = [[None, "^", "A"], ["<", "v", ">"]]

numeric_start = (2, 3)

directional_start = (2, 0)

example_input = "029A"
example_code = list(example_input)


def get_directional_value(point: Point) -> str:
    return directional[point[1]][point[0]]


def combine_lists(lists: List[List[str]]) -> List[str]:
    return ["".join(comb) for comb in product(*lists)]


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
def go_dir_for_code(code: str):
    for a, b in zip("A" + code, code):
        print(f"Going from {a} to {b}")
        yield go_directional(find_char_in_directional(a), find_char_in_directional(b))


@cache
# @logger
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

    print(f"Paths are {paths}")
    return paths


@cache
def dir_len(start: Point, end: Point) -> int:
    return len(go_directional(start, end)[0])


@cache
def is_legal_numeric_move(x: int, y: int) -> bool:
    return numeric[y][x] is not None


@cache
# @logger
def find_char_in_numeric(char: str) -> Point:
    for y, row in enumerate(numeric):
        for x, cell in enumerate(row):
            if cell == char:
                return x, y
    raise ValueError(f"Char {char} not found in numeric {numeric}")


@cache
@logger
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


def get_directional_paths(
    possible_codes: List[List[str]],
) -> Generator[List[str]]:
    start = directional_start
    paths = []
    for code in possible_codes:
        paths_for_code = []
        for char in code:
            end = find_char_in_directional(char)
            paths_for_code += [go_directional(start, end)]
            start = end

        # yield combine_lists(paths_for_code), code
        paths.append(combine_lists(paths_for_code))

    min_len = float("inf")
    for path in paths:
        if len(path[0]) < min_len:
            min_len = len(path[0])

    for path in paths:
        if len(path[0]) == min_len:
            yield path


def code_to_numeric(code: List[str]) -> int:
    return int("".join(code).replace("A", ""))


##################################### DFS #####################################


@cache
# @logger
def get_shortest_len_for_code_dfs(start: Point, end: Point, depth=24):
    if depth == 1:
        return dir_len(start, end)

    shortest = float("inf")
    sequences = go_directional(start, end)
    # print(f"Sequences are {sequences} for {get_directional_value(start)} -> {get_directional_value(end)}")
    for seq in sequences:
        length = 0
        print(f"Combo is {seq}: depth is {depth}")
        for a, b in zip("A" + seq, seq):
            print(f"Going down {a} {b}")
            tmp = get_shortest_len_for_code_dfs(
                find_char_in_directional(a), find_char_in_directional(b), depth - 1
            )
            length += tmp
            print(f"Length is for {a} -> {b} = {tmp} | depth is {depth}")
        shortest = min(shortest, length)
    return shortest


def solve_code_dfs(code: List[str], depth=24) -> int:
    result = 0
    for paths, _, _ in get_numeric_paths(code):
        shortest = float("inf")
        print(f"Paths are {paths}")

        for path in paths:
            print(f"Path is {path}")
            length = 0
            for a, b in zip("A" + path, path):
                print(f"Calculating {a} -> {b}")
                length += get_shortest_len_for_code_dfs(
                    find_char_in_directional(a), find_char_in_directional(b), depth
                )
            shortest = min(shortest, length)
        result += shortest
    return result * code_to_numeric(code)


if __name__ == "__main__":

    print("\n\n ---------   Testing     ---------\n\n")
    # start = find_char_in_directional("A")
    # end = find_char_in_directional("<")
    # print(f"Go from {get_directional_value(start)} to {get_directional_value(end)}")

    # resp = get_shortest_len_for_code_dfs(start, end, 2)
    # print(f"Result is {resp}")

    # for elem in go_dir_for_code("<A"):
    #     print(elem)

    print(solve_code_dfs(example_code, 25))

    print("\n\n ---------   Example     ---------\n\n")

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
        result += solve_code_dfs(list(code), 25)
    print(f"Result is {result}")
