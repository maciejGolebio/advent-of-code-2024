from typing import List, Tuple


def read_input(
    filename="input.txt",
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
distances[start[1]][start[0]] = 0

SHORTER = 100 if len(racetrack) > 100 else 50

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


def find_cuts_part2(
    rows: int,
    cols: int,
) -> int:
    counter = 0
    counted = set()
    for i in range(cols):
        for j in range(rows):

            if racetrack[j][i] == "#":
                continue

            for radius in range(1, 21):

                for dj in range(radius + 1):
                    di = radius - dj

                    for next_j, next_i in {
                        (j + dj, i + di),
                        (j + dj, i - di),
                        (j - dj, i + di),
                        (j - dj, i - di),
                    }:
                        if next_i < 0 or next_i >= cols or next_j < 0 or next_j >= rows:
                            continue

                        if racetrack[next_j][next_i] == "#":
                            continue

                        if (
                            distances[j][i] - distances[next_j][next_i]
                            >= (SHORTER + radius)
                            and (j, i, next_j, next_i) not in counted
                        ):
                            # counted.add((j, i, next_j, next_i))
                            # print(j, i, next_j, next_i)
                            counter += 1
    return counter


if __name__ == "__main__":

    start, end = find_start_end(racetrack)
    draw_distances(start[0], start[1], end[0], end[1], rows, cols)
    print(find_cuts_part2(rows, cols))

# 68974 - too low
# 74131 - too low
# 148262 - too low
# 2265360 >= 102 wrong
# 2170110 >= 100 + radios wrong
# 2170110 range(1, 21) -> range(2, 21) wrong
# 1085055 - remove abs wrong
# 1075121 - 100 + radius + 1 wrong
# 982425 wih set
