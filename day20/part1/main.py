from heapq import heappush, heappop
from typing import Dict, List, Tuple


def read_input(
    filename="/Users/maciejgolebiowski/private/advent2024/day20/part1/input.txt",
) -> List[List[str]]:
    with open(filename) as file:
        return [list(line.strip()) for line in file]


def pprint_track(racetrack: List[List[str]]):
    for tile in racetrack:
        print(" ".join(tile))


def pprint_distances(distances: List[List[int]]):
    for row in distances:
        print(" ".join(["{: >2}".format(str(cell)) for cell in row]))


def find_start_end(racetrack: List[List[str]]) -> Tuple[int, int]:
    start = end = None
    for y, row in enumerate(racetrack):
        for x, tile in enumerate(row):
            if tile == "S":
                start = (x, y)
            elif tile == "E":
                end = (x, y)
    return start, end


racetrack = read_input()
cols = len(racetrack)
rows = len(racetrack[0])
distances = [[-1] * cols for _ in range(rows)]
start, end = find_start_end(racetrack)
print(start, end)
distances[start[1]][start[0]] = 0


DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def draw_distances(
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    rows: int,
    cols: int,
) -> int:
    next_x = start_x
    next_y = start_y
    while next_x != end_x or next_y != end_y:
        for dx, dy in DIRECTIONS:
            x = next_x + dx
            y = next_y + dy
            if x < 0 or x >= cols or y < 0 or y >= rows:
                continue
            if racetrack[y][x] == "#":
                continue
            if distances[y][x] != -1:
                continue

            distances[y][x] = distances[next_y][next_x] + 1
            next_x, next_y = x, y


def find_cuts_part1(
    rows: int,
    cols: int,
) -> int:
    counter = 0

    for i in range(cols):
        for j in range(rows):
            if racetrack[j][i] == "#":
                continue

            for next_j, next_i in [  # half of cases
                (j + 2, i),
                (j + 1, i + 1),
                (j, i + 2),
                (j - 1, i + 1),
            ]:
                if next_i < 0 or next_i >= cols or next_j < 0 or next_j >= rows:
                    continue

                if racetrack[next_j][next_i] == "#":
                    continue

                if (value := abs(distances[j][i] - distances[next_j][next_i])) >= 102:
                    counter += 1
                    print(f"Cut at {i}, {j} and {next_i}, {next_j} with value {value}")
    return counter


if __name__ == "__main__":

    start, end = find_start_end(racetrack)
    draw_distances(start[0], start[1], end[0], end[1], rows, cols)
    print(start, end)
    # pprint_distances(distances)
    print(find_cuts_part1(rows, cols))

# 16198 too high
# 1259 - ? >
# 1289 - ? >=
