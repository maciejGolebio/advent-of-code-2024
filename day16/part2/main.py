import heapq
from typing import List, Tuple
from collections import deque


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


def find_end(maze: List[List[str]]) -> Tuple[int, int]:
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == "E":
                return x, y
    raise ValueError("No end found in maze")


def dijkstra(maze: List[List[str]]):
    start_x, start_y, end_x, end_y = *find_start(maze), *find_end(maze)
    rows = len(maze)
    cols = len(maze[0])
    start_direction = (1, 0)
    pq = []
    heapq.heappush(pq, (0, start_x, start_y, start_direction[0], start_direction[1]))
    visited = {}

    while pq:
        cost, x, y, dx, dy = heapq.heappop(pq)

        state = (x, y, dx, dy)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

        if (x, y) == (end_x, end_y):
            # don;t break here, we need to find all optimal paths
            pass

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

    return visited, (end_x, end_y)


def find_shortest_path_tiles(visited: dict, end: Tuple[int, int]) -> int:
    end_x, end_y = end
    # Find minimal cost to reach E
    end_states = [
        (x, y, dx, dy) for (x, y, dx, dy) in visited if (x, y) == (end_x, end_y)
    ]
    if not end_states:
        return 0
    min_cost = min(visited[s] for s in end_states)
    end_states = [s for s in end_states if visited[s] == min_cost]

    
    in_shortest_path = set(end_states)
    shortest_path_tiles = {(end_x, end_y)}

    queue = deque(end_states)

    def inverse_clockwise(dx, dy):
        return get_new_direction_anticlockwise(dx, dy)

    def inverse_anticlockwise(dx, dy):
        return get_new_direction_clockwise(dx, dy)

    while queue:
        x, y, dx, dy = queue.popleft()
        c = visited[(x, y, dx, dy)]

        # Forward predecessor
        fx, fy = x - dx, y - dy
        prev_cost = c - 1
        if (
            prev_cost >= 0
            and (fx, fy, dx, dy) in visited
            and visited[(fx, fy, dx, dy)] == prev_cost
        ):
            if (fx, fy, dx, dy) not in in_shortest_path:
                in_shortest_path.add((fx, fy, dx, dy))
                shortest_path_tiles.add((fx, fy))
                queue.append((fx, fy, dx, dy))

        # Clockwise predecessor
        prev_cost = c - 1000
        if prev_cost >= 0:
            # current_dir = clockwise(prev_dir) => prev_dir = inverse_clockwise(current_dir)
            prev_dx, prev_dy = inverse_clockwise(dx, dy)
            if (x, y, prev_dx, prev_dy) in visited and visited[
                (x, y, prev_dx, prev_dy)
            ] == prev_cost:
                if (x, y, prev_dx, prev_dy) not in in_shortest_path:
                    in_shortest_path.add((x, y, prev_dx, prev_dy))
                    shortest_path_tiles.add((x, y))
                    queue.append((x, y, prev_dx, prev_dy))

        # Anticlockwise predecessor
        prev_cost = c - 1000
        if prev_cost >= 0:
            # current_dir = anticlockwise(prev_dir) => prev_dir = inverse_anticlockwise(current_dir)
            prev_dx, prev_dy = inverse_anticlockwise(dx, dy)
            if (x, y, prev_dx, prev_dy) in visited and visited[
                (x, y, prev_dx, prev_dy)
            ] == prev_cost:
                if (x, y, prev_dx, prev_dy) not in in_shortest_path:
                    in_shortest_path.add((x, y, prev_dx, prev_dy))
                    shortest_path_tiles.add((x, y))
                    queue.append((x, y, prev_dx, prev_dy))

    return len(shortest_path_tiles)


if __name__ == "__main__":
    # Load your maze input here
    maze = read_input("input.txt")  # Replace with your input file
    visited, end = dijkstra(maze)
    # Print the minimal cost
    end_states = [(x, y, dx, dy) for (x, y, dx, dy) in visited if (x, y) == end]
    if not end_states:
        print("No path found.")
    else:
        min_cost = min(visited[s] for s in end_states)
        print("Lowest cost:", min_cost)
        # Find how many tiles are on at least one best path
        tile_count = find_shortest_path_tiles(visited, end)
        print("Tiles on at least one best path:", tile_count)
