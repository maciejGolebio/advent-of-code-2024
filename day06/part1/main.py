print_map = lambda m: print("\n".join(["".join(x) for x in m]))


UP = "^"
DOWN = "V"
LEFT = "<"
RIGHT = ">"
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


def is_collision(map, position):
    i, j = position
    return map[i][j] == "#"


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


def get_out(map, position, direction):
    while not is_out(map, position):
        mark_position(map, position, "X")
        position, collision = move(map, position, direction)
        if collision:
            direction = change_direction(direction)
            continue
        mark_position(map, position, direction)
        position

def count_steps(map):
    counter = 0
    for row in map:
        for cell in row:
            if cell == "X" or cell in DIRECTIONS:
                counter += 1
    return counter


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

    print(position)
    print_map(maps)
    print("---------")
    get_out(maps, position, UP)
    print_map(maps)
    print(count_steps(maps))
