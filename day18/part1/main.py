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
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            if counter == limit:
                break
            x, y = map(int, line.strip().split(","))
            print(x, y)
            memory[y][x] = "#"
            counter += 1

    return memory


def dijkstra(memory: List[List[str]], size=71):
    start_x, start_y, end_x, end_y = 0, 0, size - 1, size - 1
    rows = len(memory)
    cols = len(memory[0])
    start_direction = (1, 0)

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
            return cost

        for new_direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + new_direction[0], y + new_direction[1]

            if new_x < 0 or new_x >= cols or new_y < 0 or new_y >= rows:
                continue

            if memory[new_y][new_x] == ".":  # not #
                memory[new_y][new_x] = memory[y][x]
                heapq.heappush(pq, (cost + 1, new_x, new_y))

    return float("inf")


def get_sum_combinations(index):
    combinations = []
    for a in range(index + 1):
        b = index - a
        combinations.append((a, b))
    return combinations


if __name__ == "__main__":
    SIZE = 71
    LIMIT = 1024
    memory = read_input("input.txt", SIZE, LIMIT)
    pprint(memory)


    for i in range(40):
        diagonal_options = get_sum_combinations(i)
        print(diagonal_options)
        
        for x, y in diagonal_options:
            
            ## check left to right
            if memory[y][x] == "#":
                continue
            copied_memory = copy.deepcopy(memory)
            copied_memory[y][x] = "#"
            result = dijkstra(copied_memory, SIZE)
            if result == float("inf"):
                print(f"Part 2: {x}, {y}")
                exit()
            else:
        
            ## check right to left
            if memory[x][y] == "#":
                continue
            copied_memory = copy.deepcopy()
            copied_memory[x][y] = "#"
            result = dijkstra(copied_memory, SIZE)
            if result == float("inf"):
                print(f"Part 2: {x}, {y}")
                exit()


    result = dijkstra(memory, SIZE)
    print(f"Part 1: {result}")

    print("Done!")
