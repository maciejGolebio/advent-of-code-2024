import heapq
from typing import List, Tuple


def read_input(filename="input.txt") -> List[List[str]]:
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
                racetrack[new_y][new_x] = racetrack[y][x]
                heapq.heappush(pq, (cost + 1, new_x, new_y))

    return float("inf")


def can_cheat(cheated: int) -> bool:
    return cheated > 0


def get_next_cheated(cheated: int) -> int:
    """
    for 2 - keeps cheating right
    for 1 - stops cheating
    for 0 - stopped cheating
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
):
    pq = []
    heapq.heappush(pq, (0, start_x, start_y, 2))

    visited = {}
    count_shorter = 0

    while pq:

        (
            cost,
            x,
            y,
            cheated,  # 0 - cheated, 1 - cheated in previous step, 2 - not cheated
        ) = heapq.heappop(pq)

        state = (x, y)
        if state in visited and visited[state] <= cost:
            continue
        
        visited[state] = cost

        if cost >= regular_cost:
            continue
            # return float("inf"), 0

        if y == end_y and x == end_x:
            count_shorter += 1
            continue
            # return cost, count_shorter

        for new_direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + new_direction[0], y + new_direction[1]

            if new_x < 0 or new_x >= cols or new_y < 0 or new_y >= rows:
                continue

            if racetrack[new_y][new_x] == "#" and can_cheat(cheated):
                heapq.heappush(pq, (cost + 1, new_x, new_y, cheated - 1))
                continue
            elif racetrack[new_y][new_x] != "#":
                heapq.heappush(pq, (cost + 1, new_x, new_y, get_next_cheated(cheated)))

    if count_shorter == 0:
        return float("inf"), 0

    return cost, count_shorter


if __name__ == "__main__":
    racetrack = read_input()
    start, end = find_start_end(racetrack)
    shortest, visited = dijkstra(
        racetrack, start[0], start[1], end[0], end[1], len(racetrack), len(racetrack[0])
    )
    print(shortest)
    print(visited)

    shortest_cheating, count_shorter = cheating_dijkstra(
        racetrack,
        start[0],
        start[1],
        end[0],
        end[1],
        len(racetrack),
        len(racetrack[0]),
        shortest,
    )
    print(f"Shortest cheating: {shortest_cheating}")
    print(f"Count shorter: {count_shorter}")
