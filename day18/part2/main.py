import copy
import heapq
from typing import List


def pprint(memory):
    for row in memory:
        print("".join(row))
    print()


def read_input(filename="input.txt", size=71, limit=1024):
    memory = [["." for _ in range(size)] for _ in range(size)]
    counter = 0
    next_elems = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            x, y = map(int, line.strip().split(","))
            if counter >= limit:
                next_elems.append((x, y))
                continue
        
            memory[y][x] = "#"
            counter += 1

    return memory, next_elems


def dijkstra(memory: List[List[str]], size=71):
    start_x, start_y, end_x, end_y = 0, 0, size - 1, size - 1
    rows = len(memory)
    cols = len(memory[0])

    pq = []
    heapq.heappush(pq, (0, start_x, start_y))

    visited = {}

    while pq:

        (cost, x, y) = heapq.heappop(pq)
        state = (x, y)
        if state in visited and visited[state] <= cost:
            continue

        visited[state] = cost

        if y == end_y and x == end_x:
            return cost

        for new_direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + new_direction[0], y + new_direction[1]

            if new_x < 0 or new_x >= cols or new_y < 0 or new_y >= rows:
                continue

            if memory[new_y][new_x] == ".":  # not #
                memory[new_y][new_x] = memory[y][x]
                heapq.heappush(pq, (cost + 1, new_x, new_y))

    return float("inf")


if __name__ == "__main__":
    SIZE = 71
    LIMIT = 1024
    memory, next_elems = read_input("input.txt", SIZE, LIMIT)
    pprint(memory)

    counter = 0

    for x, y in next_elems:
        print(f'Processing {x}, {y} - {counter}')
        counter += 1

        memory[y][x] = "#"
        result = dijkstra(memory, SIZE)
        if result == float("inf"):
            print(f"Part 2: {x}, {y}")
            exit()

    print("Done!")