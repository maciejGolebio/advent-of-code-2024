import copy
from typing import List, Tuple


def full_logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: { args }\n")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned: {result}\n")
        return result

    return wrapper


def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: { args[1:] }\n")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned: {result}\n")
        return result

    return wrapper


def to_warehouse_line(line: str) -> List[str]:
    splitted_line = list(line.strip())
    new_line = []
    for i in range(len(splitted_line)):
        if splitted_line[i] == "@":
            new_line.append("@")
            new_line.append(".")

        if splitted_line[i] == "#":
            new_line.append("#")
            new_line.append("#")

        if splitted_line[i] == ".":
            new_line.append(".")
            new_line.append(".")

        if splitted_line[i] == "O":
            new_line.append("[")
            new_line.append("]")

    return new_line


def read_input() -> Tuple[List[List[str]], List[str]]:
    warehouse = []
    commands = []

    with open("input.txt", "r") as file:
        lines = file.read().splitlines()
        for line in lines:
            if line[0] == "<" or line[0] == ">" or line[0] == "^" or line[0] == "v":
                commands += list(line.strip())
                continue
            warehouse.append(to_warehouse_line(line))

    return warehouse, commands


class Point:

    def __init__(self, x, y, type="Point"):
        self.x = x
        self.y = y
        self.type = type

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"{self.type}({self.x}, {self.y})"

    def __repr__(self):
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


def move_point_with_scale(point: Point, vector: Vector, scale: int) -> Point:
    return Point(point.x + (vector.x * scale), point.y + (vector.y * scale))


@full_logger
def get_box_next_points(
    current_left_bracket: Point, command: Vector
) -> Tuple[Point, Point]:
    current_right_bracket = Point(current_left_bracket.x + 1, current_left_bracket.y)
    return move_point_with_scale(
        current_left_bracket, command, 2
    ), move_point_with_scale(current_right_bracket, command, 2)


@logger
def get_left_bracket_position(warehouse: List[List[str]], candidate: Point) -> Point:
    # candidate is '[' or ']'
    x, y = candidate.x, candidate.y
    if warehouse[y][x] == "[":
        return candidate
    if warehouse[y][x] == "]":
        return Point(x - 1, y)
    raise ValueError(f"Invalid candidate: {candidate}")


@logger
def eventually_push_boxes_2(
    warehouse: List[List[str]],
    current_left_bracket: Point,
    command: Vector,
    new_left_brackets: List[Point],
) -> bool:

    next_left_bracket, next_right_bracket = get_box_next_points(
        current_left_bracket, command
    )

    new_left_brackets.append(current_left_bracket)
    new_left_brackets.append(next_right_bracket)

    left_x, left_y, right_x, right_y = (
        next_left_bracket.x,
        next_left_bracket.y,
        next_right_bracket.x,
        next_right_bracket.y,
    )

    if warehouse[left_y][left_x] == "#" or warehouse[right_y][right_x] == "#":
        # Wall detected
        return False

    if (
        warehouse[left_y][left_x] == "."
        and warehouse[right_y][right_x] == "."
        and command.y != 0
    ):
        # Empty space, move the box down or up
        new_left_brackets.append(next_left_bracket)
        return new_left_brackets

    if (warehouse[left_y][left_x] == "." and command.x == -1) or (
        warehouse[right_y][right_x] == "." and command.x == 1
    ):
        # Empty space, move the box left or right
        if command.x == -1:
            new_left_brackets.append(next_right_bracket)
        else:
            new_left_brackets.append(next_left_bracket)
        return True

    if (
        warehouse[left_y][left_x] == "["
        or warehouse[right_y][right_x] == "]"
        and command.x != 0
    ):
        # Box detected - simple move left or right
        if eventually_push_boxes_2(
            warehouse,
            move_point_with_scale(current_left_bracket, command, 2),
            command,
            new_left_brackets,
        ):
            if command.x == -1:
                new_left_brackets.append(
                    Point(current_left_bracket.x - 1, current_left_bracket.y)
                )
            if command.x == 1:
                new_left_brackets.append(
                    Point(current_left_bracket.x + 1, current_left_bracket.y)
                )
            return True
        else:
            return False

    if (
        warehouse[left_y][left_x] == "["
        or warehouse[right_y][right_x] == "]"
        and command.y != 0
    ):
        # Box detected - simple move up or down
        if eventually_push_boxes_2(
            warehouse,
            move_point_with_scale(current_left_bracket, command, 1),
            command,
            new_left_brackets,
        ):
            return True
        else:
            return False

    if (
        warehouse[left_y][left_x] == "]"
        or warehouse[right_y][right_x] == "["
        and command.y != 0
    ):  # Pyramid move
        left, right = False, False
        if (
            warehouse[left_y][left_x] == "]"
            and eventually_push_boxes_2(
                warehouse,
                Point(left_x - 1, left_y + command.y),
                command,
                new_left_brackets,
            )
        ) or warehouse[left_y][left_x] != "]":
            left = True

        if (
            warehouse[right_y][right_x] == "["
            and eventually_push_boxes_2(
                warehouse,
                move_point_with_scale(next_right_bracket, command, 1),
                command,
                new_left_brackets,
            )
        ) or warehouse[right_y][right_x] != "[":
            right = True

        return left and right


@logger
def eventually_push_boxes(
    warehouse: List[List[str]], current_left_bracket: Point, command: Vector
) -> bool:

    next_left_bracket, next_right_bracket = get_box_next_points(
        current_left_bracket, command
    )

    left_x, left_y, right_x, right_y = (
        next_left_bracket.x,
        next_left_bracket.y,
        next_right_bracket.x,
        next_right_bracket.y,
    )

    if warehouse[left_y][left_x] == "#" or warehouse[right_y][right_x] == "#":
        # Wall detected
        return False

    if (
        warehouse[left_y][left_x] == "."
        and warehouse[right_y][right_x] == "."
        and command.y != 0
    ):
        # Empty space, move the box down or up
        warehouse[left_y][left_x] = "["
        warehouse[right_y][right_x] = "]"
        return True

    if (warehouse[left_y][left_x] == "." and command.x == -1) or (
        warehouse[right_y][right_x] == "." and command.x == 1
    ):
        # Empty space, move the box left or right
        if command.x == -1:
            warehouse[right_y][right_x] = "["
            warehouse[right_y][right_x + 1] = "]"
        else:  # command.x == 1
            warehouse[left_y][left_x] = "]"
            warehouse[left_y][left_x - 1] = "["
        return True

    if (
        warehouse[left_y][left_x] == "["
        or warehouse[right_y][right_x] == "]"
        and command.y != 0
    ):
        # Box detected
        print("Simple move LEFT/RIGHT")
        if eventually_push_boxes(
            warehouse, move_point_with_scale(current_left_bracket, command, 2), command
        ):
            # If the box was moved hori, move the current box
            if command.x == -1:
                warehouse[current_left_bracket.y][current_left_bracket.x] = "]"
                warehouse[current_left_bracket.y][current_left_bracket.x - 1] = "["

            if command.x == 1:
                warehouse[current_left_bracket.y][current_left_bracket.x] = "["
                warehouse[current_left_bracket.y][current_left_bracket.x + 1] = "]"

            return True
        else:
            return False

    if (
        warehouse[left_y][left_x] == "["
        or warehouse[right_y][right_x] == "]"
        and command.x != 0
    ):
        # Box detected
        print("Simple move UP/DOWN")
        if eventually_push_boxes(
            warehouse, move_point_with_scale(current_left_bracket, command, 1), command
        ):
            return True
        else:
            return False

    if warehouse[left_y][left_x] == "]" or warehouse[right_y][right_x] == "[":
        print("Pyramid move")
        # Box detected, only possible when up or down

        if eventually_push_boxes(
            warehouse,
            move_point_with_scale(
                next_left_bracket,
                command,
                1,
            ),
            command,
        ):
            print(f"Swapping boxes, current: {current_left_bracket}")
            # If the box was moved hori, move the current box

            return True
        else:
            return False

    return False


@logger
def move_robot(warehouse: List[List[str]], current: Point, command: Vector) -> Point:
    working_warehouse = copy.deepcopy(warehouse)
    working_warehouse[current.y][current.x] = "."
    new_robot_position = move_point(current, command)
    x, y = new_robot_position.x, new_robot_position.y
    
    moves = []

    if warehouse[y][x] == "#":
        # Wall detected
        return current

    if warehouse[y][x] == ".":
        # Empty space, move the robot
        warehouse[y][x] = "@"
        warehouse[current.y][current.x] = "."
        return new_robot_position

    if warehouse[y][x] == "[" and command.x != 0:
        new_left = Point(x + 1, y)
        if eventually_push_boxes_2(working_warehouse, new_left, command, moves):
            working_warehouse[y][x] = "@"
            working_warehouse[current.y][current.x] = "."
            return new_robot_position

    if warehouse[y][x] == "]" and command.x != 0:
        new_left = Point(x - 1, y + command.y)
        if eventually_push_boxes_2(working_warehouse, new_left, command, moves):
            working_warehouse[y][x] = "@"
            working_warehouse[current.y][current.x] = "."
            return new_robot_position

    if warehouse[y][x] == "[" and command.y != 0:
        new_left = move_point_with_scale(Point(x, y), command, 1)
        if eventually_push_boxes(working_warehouse, new_left, command):
            working_warehouse[y][x] = "@"
            working_warehouse[y][x + 1] = "."
            working_warehouse[current.y][current.x] = "."
            return new_robot_position

    if warehouse[y][x] == "]" and command.y != 0:
        new_left = move_point_with_scale(Point(x, y), command, 1)
        if eventually_push_boxes(working_warehouse, new_left, command):
            working_warehouse[y][x] = "@"
            working_warehouse[y][x - 1] = "."
            working_warehouse[current.y][current.x] = "."
            return new_robot_position

    return current


def print_warehouse(warehouse: List[List[str]]) -> None:
    print("\n")
    for row in warehouse:
        print("".join(row))
    print("\n")


def sum_warehouse(warehouse: List[List[str]]) -> int:
    result = 0
    warehouse_formula = lambda i, j: 100 * i + j
    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == "[":
                result += warehouse_formula(i, j)
    return result


if __name__ == "__main__":
    warehouse, commands = read_input()
    print_warehouse(warehouse)
    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == "@":
                robot = Point(j, i)
                print(f"Robot found at {robot} {i} {j}")
                break

    for command in commands:
        robot = move_robot(warehouse, robot, command_to_vector(command))

    print_warehouse(warehouse)
    print(sum_warehouse(warehouse))
