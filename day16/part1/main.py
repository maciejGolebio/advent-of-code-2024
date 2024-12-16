import heapq
from typing import List, Tuple


def print_maze(maze: List[List[str]]):
    print("\n".join(["".join(row) for row in maze]))


def get_new_direction_clockwise(dx: int, dy: int) -> Tuple[int, int]:
    if (dx, dy) == (0, 1):  # down
        return (-1, 0)  # left
    elif (dx, dy) == (-1, 0):  # left
        return (0, -1)  # up
    elif (dx, dy) == (0, -1):  # up
        return (1, 0)  # right
    elif (dx, dy) == (1, 0):  # right
        return (0, 1)  # down


def get_new_direction_anticlockwise(dx: int, dy: int) -> Tuple[int, int]:
    if (dx, dy) == (0, 1):  # down
        return (1, 0)  # right
    elif (dx, dy) == (1, 0):  # right
        return (0, -1)  # up
    elif (dx, dy) == (0, -1):  # up
        return (-1, 0)  # left
    elif (dx, dy) == (-1, 0):  # left
        return (0, 1)  # down


def read_input(file_path: str = "input.txt") -> List[List[str]]:
    maze = []
    with open(file_path, "r") as file:
        for line in file.readlines():
            maze.append(list(line.strip()))
    return maze


def find_start(maze: List[List[str]]) -> Tuple[int, int]:
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == "S":
                return x, y
    raise ValueError("No start found in maze")


def dijkstra(maze: List[List[str]]) -> float:
    start_x, start_y = find_start(maze)
    start_direction = (1, 0)
    rows = len(maze)
    cols = len(maze[0])

    # Priority queue: (cost, x, y, dx, dy)
    pq = []
    heapq.heappush(pq, (0, start_x, start_y, start_direction[0], start_direction[1]))

    # visited[(x,y,dx,dy)] = best cost so far
    visited = {}

    while pq:
        cost, x, y, dx, dy, path = heapq.heappop(pq)

        # Cut off if we have already visited this state with a lower cost
        state = (x, y, dx, dy)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

        # Check if this is the end
        if maze[y][x] == "E":
            return cost, path

        # Move forward
        nx, ny = x + dx, y + dy
        if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] != "#":
            forward_cost = cost + 1
            forward_state = (nx, ny, dx, dy)
            if forward_state not in visited or visited[forward_state] > forward_cost:
                heapq.heappush(pq, (forward_cost, nx, ny, dx, dy))

        # Turn clockwise
        ndx, ndy = get_new_direction_clockwise(dx, dy)
        cw_cost = cost + 1000
        cw_state = (x, y, ndx, ndy)
        if cw_state not in visited or visited[cw_state] > cw_cost:
            heapq.heappush(pq, (cw_cost, x, y, ndx, ndy))

        # Turn anticlockwise
        ndx, ndy = get_new_direction_anticlockwise(dx, dy)
        acw_cost = cost + 1000
        acw_state = (x, y, ndx, ndy)
        if acw_state not in visited or visited[acw_state] > acw_cost:
            heapq.heappush(pq, (acw_cost, x, y, ndx, ndy))

    return float("inf")


if __name__ == "__main__":
    maze = read_input()
    lowest_cost = dijkstra(maze)
    print("Lowest cost:", lowest_cost)
