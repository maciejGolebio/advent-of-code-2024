from typing import List, Tuple


def read_input() -> Tuple[List[List[str]], List[str]]:
    warehouse = []
    commands = []

    with open("input.txt", "r") as file:
        lines = file.read().splitlines()
        for line in lines:
            if line[0] == "<" or line[0] == ">" or line[0] == "^" or line[0] == "v":
                commands += list(line.strip())
                continue
            warehouse.append(list(line.strip()))

    return warehouse, commands


class Point:

    def __init__(self, x, y, type="Point"):
        self.x = x
        self.y = y
        self.type = type

    def __str__(self):
        return f"{self.type}({self.x}, {self.y})"


class Vector(Point):

    def __init__(self, x, y):
        super().__init__(x, y, "Vector")


def command_to_vector(command: str) -> Vector:
    if command == "<":
        return Vector(-1, 0)
    elif command == ">":
        return Vector(1, 0)
    elif command == "^":
        return Vector(0, -1)
    elif command == "v":
        return Vector(0, 1)
    else:
        raise ValueError(f"Invalid command: {command}")


def move_point(point: Point, vector: Vector) -> Point:
    return Point(point.x + vector.x, point.y + vector.y)


def eventually_push_boxes(
    warehouse: List[List[str]], current_box: Point, command: Vector
) -> bool:
    new_box_position = move_point(current_box, command)
    x, y = new_box_position.x, new_box_position.y

    if warehouse[y][x] == "#":
        # Wall detected
        return False

    if warehouse[y][x] == ".":
        # Empty space, move the box
        warehouse[y][x] = "O"
        return True

    if warehouse[y][x] == "O":
        # Box detected
        if eventually_push_boxes(warehouse, new_box_position, command):
            # If the box was moved, move the current box
            # warehouse[y][x] = "O"
            return True
        else:
            return False

    return False


def move_robot(warehouse: List[List[str]], current: Point, command: Vector) -> None:
    new_robot_position = move_point(current, command)
    x, y = new_robot_position.x, new_robot_position.y

    if warehouse[y][x] == "#":
        # Wall detected
        return

    if warehouse[y][x] == ".":
        # Empty space, move the robot
        warehouse[y][x] = "@"
        warehouse[current.y][current.x] = "."
        current.x = x
        current.y = y

    if warehouse[y][x] == "O" and eventually_push_boxes(
        warehouse, new_robot_position, command
    ):
        # Box detected and moved
        warehouse[y][x] = "@"
        warehouse[current.y][current.x] = "."
        current.x = x
        current.y = y

def print_warehouse(warehouse: List[List[str]]) -> None:
    for row in warehouse:
        print("".join(row))



def sum_warehouse(warehouse: List[List[str]]) -> int:
    result = 0
    warehouse_formula = lambda i, j: 100 * i + j
    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == "O":
                result += warehouse_formula(i, j)
    return result

if __name__ == "__main__":
    warehouse, commands = read_input()
    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == "@":
                robot = Point(j, i)
                break

    for command in commands:
        move_robot(warehouse, robot, command_to_vector(command))
    
    print_warehouse(warehouse)
    print(sum_warehouse(warehouse))