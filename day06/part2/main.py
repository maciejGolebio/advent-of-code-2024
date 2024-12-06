print_map = lambda m: print("\n".join(["".join(x) for x in m]))


UP = "^"
DOWN = "V"
LEFT = "<"
RIGHT = ">"
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


def is_collision(map, position):
    i, j = position
    mark = map[i][j]
    return mark == "#" or mark == "O"


def change_direction(direction):
    if direction == UP:
        return RIGHT
    elif direction == RIGHT:
        return DOWN
    elif direction == DOWN:
        return LEFT
    elif direction == LEFT:
        return UP
    raise Exception("Invalid direction")


def move(map, position, direction):
    i, j = position
    if direction == UP and not is_collision(map, (i - 1, j)):
        return (i - 1, j), False
    elif direction == DOWN and not is_collision(map, (i + 1, j)):
        return (i + 1, j), False
    elif direction == LEFT and not is_collision(map, (i, j - 1)):
        return (i, j - 1), False
    elif direction == RIGHT and not is_collision(map, (i, j + 1)):
        return (i, j + 1), False
    else:
        return position, True


def is_out(map, position):
    i, j = position
    # print(f"is_out: {i} {j}, len i: {len(map)}, len j: {len(map[0])}")
    return i <= 0 or j <= 0 or i >= len(map) - 1 or j >= len(map[0]) - 1


def mark_position(map, position, mark):
    i, j = position
    map[i][j] = mark


def is_repetition(position_map, position, direction):
    i, j = position
    return direction in position_map[i][j]


def get_out(map, position, direction, position_map):
    repetition = False
    while not is_out(map, position):
        mark_position(map, position, "X")
        position, collision = move(map, position, direction)
        
        if collision:
            direction = change_direction(direction)
            continue
        
        if is_repetition(position_map, position, direction):
            repetition = True
            break
        
        position_map[position[0]][position[1]].append(direction)
        mark_position(map, position, direction)
        

    return repetition


def get_all_positions(map):
    positions = []
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] in DIRECTIONS or map[i][j] == "X":
                positions.append((i, j))
    return positions


if __name__ == "__main__":
    maps = []

    position = (0, 0)
    with open("input.txt") as f:

        lines = f.readlines()
        row = []
        i = 0

        for line in lines:
            j = 0
            for c in line:
                if c == "\n":
                    maps.append(row)
                    row = []
                else:
                    if c in DIRECTIONS:
                        position = (i, j)
                    row.append(c)
                j += 1
            i += 1

    copied_map = [row[:] for row in maps]
    print(position)
    print_map(maps)
    print("---------\n")

    position_map = [[[] for _ in range(len(maps[0]))] for _ in range(len(maps))]
    
    get_out(maps, position, UP, position_map)
    print_map(maps)
    print("\n---------\n")
    candidate_obstacle_positions = get_all_positions(maps)

    counter = 0
    for candidate in candidate_obstacle_positions:
        cp_maps = [row[:] for row in copied_map]
        position_map = [[ [] for _ in range(len(maps[0]))] for _ in range(len(maps))]
        cp_maps[candidate[0]][candidate[1]] = "O"
        if get_out(cp_maps, position, UP, position_map):
            print('\n-----------')
            print_map(cp_maps)
            print('\n-----------')
            counter += 1
    
    print(counter)
    print(f'Length of candidate_obstacle_positions: {len(candidate_obstacle_positions)}')