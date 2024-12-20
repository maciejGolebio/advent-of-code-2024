from collections import deque
import copy
from functools import cache
import heapq
from typing import List, Set, Tuple


def read_input(
    filename="/Users/maciejgolebiowski/private/advent2024/day20/part1/input.txt",
) -> List[List[str]]:
    with open(filename) as file:
        return [list(line.strip()) for line in file]


def pprint(racetrack: List[List[str]]):
    for tile in racetrack:
        print("".join(tile))


def find_start_end(racetrack: List[List[str]]) -> Tuple[int, int]:
    start = end = None
    for y, row in enumerate(racetrack):
        for x, tile in enumerate(row):
            if tile == "S":
                start = (x, y)
            elif tile == "E":
                end = (x, y)
    return start, end


def dijkstra(
    racetrack: List[List[str]],
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    rows: int,
    cols: int,
) -> int:
    print(start_x, start_y, end_x, end_y)

    pq = []
    heapq.heappush(pq, (0, start_x, start_y))

    visited = {}

    while pq:

        (
            cost,
            x,
            y,
        ) = heapq.heappop(pq)

        state = (x, y)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

        if y == end_y and x == end_x:
            return cost, visited

        for new_direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + new_direction[0], y + new_direction[1]

            if new_x < 0 or new_x >= cols or new_y < 0 or new_y >= rows:
                continue

            if racetrack[new_y][new_x] != "#":
                heapq.heappush(pq, (cost + 1, new_x, new_y))

    return float("inf")


def can_cheat(cheated: int) -> bool:
    return cheated > 0


def get_next_cheated(cheated: int) -> int:
    """
    for 2 - keeps cheating => returns 2\n
    for 1 - stops cheating => returns 0\n
    for 0 - stopped cheating => returns 0
    """
    if cheated == 2:
        return 2
    return 0


def cheating_dijkstra(
    racetrack: List[List[str]],
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    rows: int,
    cols: int,
    regular_cost: int,
    forbidden_combo: Set[Tuple[int, int, int, int]],
):
    visited = {}
    pq = []
    heapq.heappush(pq, (0, start_x, start_y, 2, -1, -1, -1, -1))

    while pq:

        (
            cost,
            x,
            y,
            cheated,  # 0 - cheated, 1 - cheated in previous step, 2 - not cheated
            start_cheated_x,
            start_cheated_y,
            stop_cheated_x,
            stop_cheated_y,
        ) = heapq.heappop(pq)

        state = (
            x,
            y,
            cheated,
            start_cheated_x,
            start_cheated_y,
            # stop_cheated_x,
            # stop_cheated_y,
        )
        if state in visited and visited[state] <= cost:
            continue

        visited[state] = cost

        if cost >= regular_cost:
            return float("inf")

        if y == end_y and x == end_x:
            print(f"End Cost: {cost}")
            # print(
            #     f"Cheat path: {start_cheated_x}, {start_cheated_y}, -> {stop_cheated_x}, {stop_cheated_y}"
            # )
            
            if start_cheated_x != -1:
                racetrack[start_cheated_y][start_cheated_x] = "1"
            if stop_cheated_x != -1:
                racetrack[stop_cheated_y][stop_cheated_x] = "2"

            # pprint(racetrack)

            if start_cheated_x != -1:
                forbidden_combo.add(
                    (start_cheated_x, start_cheated_y, stop_cheated_x, stop_cheated_y)
                )
            return cost

        for new_direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + new_direction[0], y + new_direction[1]

            if new_x < 0 or new_x >= cols or new_y < 0 or new_y >= rows:
                continue

            if racetrack[new_y][new_x] == "#":
                if (
                    cheated == 2 and (new_x, new_y, -1, -1) not in forbidden_combo
                ):  # start cheating
                    heapq.heappush(
                        pq,
                        (
                            cost + 1,
                            new_x,
                            new_y,
                            1,
                            new_x,
                            new_y,
                            -1,
                            -1,
                        ),
                    )
                    # racetrack[new_y][new_x] = "W"
                elif (
                    cheated == 1
                    and (start_cheated_x, start_cheated_y, new_x, new_y)
                    not in forbidden_combo
                    and racetrack[new_y][new_x] != "#"

                ):
                    heapq.heappush(
                        pq,
                        (
                            cost + 1,
                            new_x,
                            new_y,
                            0,
                            start_cheated_x,
                            start_cheated_y,
                            new_x,
                            new_y,
                        ),
                    )
                    #racetrack[new_y][new_x] = "U"
                else:
                    continue

            elif racetrack[new_y][new_x] != "#":
                heapq.heappush(
                    pq,
                    (
                        cost + 1,
                        new_x,
                        new_y,
                        get_next_cheated(cheated),
                        start_cheated_x,
                        start_cheated_y,
                        stop_cheated_x,
                        stop_cheated_y,
                    ),
                )

    return float("inf")


def count_cheated(racetrack, normally_shortest, start, end):
    forbidden_to_cheat_combos = set()
    count = 0
    shorter_than_normal = 0
    saves = {}
    
    while shorter_than_normal < normally_shortest or shorter_than_normal == float(
        "inf"
    ):
        copied_racetrack = copy.deepcopy(racetrack)
        shorter_than_normal = cheating_dijkstra(
            copied_racetrack,
            start[0],
            start[1],
            end[0],
            end[1],
            len(racetrack),
            len(racetrack[0]),
            normally_shortest,
            forbidden_to_cheat_combos,
        )
        print(f"Shorter: {shorter_than_normal}, normal: {normally_shortest}")
        if shorter_than_normal < normally_shortest:
            saved = normally_shortest - shorter_than_normal
            if saved not in saves:
                saves[saved] = 0
            saves[saved] += 1
            count += 1
        else:
            break

    for k, v in saves.items():
        print(f"{k}: {v}")
    return count


if __name__ == "__main__":
    racetrack = read_input()
    start, end = find_start_end(racetrack)
    # pprint(racetrack)
    normally_shortest, _ = dijkstra(
        racetrack, start[0], start[1], end[0], end[1], len(racetrack), len(racetrack[0])
    )
    print(f"Shortest: {normally_shortest}")

    count = count_cheated(racetrack, normally_shortest, start, end)

    print(f"Count: {count}")
