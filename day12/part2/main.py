import copy
from typing import Dict, List, Set

VISITED = "."


def eventually_print(should_print, *args):
    if should_print:
        print(*args)


class Point:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __eq__(self, value: "Point"):
        return self.i == value.i and self.j == value.j

    def __hash__(self):
        return hash((self.i, self.j))

    def __gt__(self, value: "Point"):
        # row is more important
        if self.i > value.i:
            return True
        if self.i == value.i and self.j > value.j:
            return True
        return False

    def __str__(self):
        return f"Point({self.i}, {self.j})"


class Line:
    # i - row
    # j - column
    def __init__(self, point1: Point, point2: Point):
        point1, point2 = sorted([point1, point2])

        self.point1 = point1
        self.point2 = point2
        self.is_side = False

    def __str__(self):
        return f"Line({self.point1}, {self.point2})"

    def __repr__(self):
        return f"Line({self.point1}, {self.point2})"

    def is_horizontal(self):
        return self.point1.i == self.point2.i

    def is_vertical(self):
        return self.point1.j == self.point2.j

    def is_continuation(self, line: "Line"):
        if self.is_horizontal() and line.is_horizontal():
            return self.__have_common_point(line)

        if self.is_vertical() and line.is_vertical():
            return self.__have_common_point(line)

        return False

    def __have_common_point(self, line: "Line"):
        return (
            self.point1 == line.point1
            or self.point1 == line.point2
            or self.point2 == line.point1
            or self.point2 == line.point2
        )

    def __find_common_point(self, line: "Line") -> Point:
        if self.point1 == line.point1 or self.point1 == line.point2:
            return self.point1
        if self.point2 == line.point1 or self.point2 == line.point2:
            return self.point2
        return None

    def set_is_side(self):
        self.is_side = True

    def __eq__(self, value: "Line"):
        if isinstance(value, Line):
            return (self.point1 == value.point1 and self.point2 == value.point2) or (
                self.point1 == value.point2 and self.point2 == value.point1
            )

        return False

    def __hash__(self):
        return hash((self.point1, self.point2))

    # region CONTINUATION IN GARDEN
    def is_continuation_in_garden_vertical(self, garden, line: "Line", should_print):
        # exclude diagonal continuation
        column = self.point1.j  # all have same j
        if (column >= len(garden[0])) or column <= 0:
            return True

        common_point = self.__find_common_point(line)
        if common_point.i + 1 > len(garden):
            raise Exception("Shouldn't go here")

        eventually_print(
            should_print,
            "[vertical]: Common point {} and column {}".format(common_point, column),
        )
        left_up_field = garden[common_point.i - 1][column - 1]
        right_up_field = garden[common_point.i - 1][column]

        left_down_field = "^"
        right_down_field = "*"

        if common_point.i + 1 < len(garden):
            left_down_field = garden[common_point.i][column - 1]
            right_down_field = garden[common_point.i][column]

        eventually_print(
            should_print,
            f"{left_up_field} | {right_up_field}\n- - -\n{left_down_field} | {right_down_field}",
        )

        if left_up_field == right_down_field:
            eventually_print(should_print, "[vertical]: Left up = Right down")
            return False
        elif right_up_field == left_down_field:
            eventually_print(should_print, "[vertical]: Right up = Left down")
            return False
        else:
            return True

    def is_continuation_in_garden_horizontal(self, garden, line: "Line", should_print):
        # exclude diagonal continuation
        row = self.point1.i  # all have same i
        if row >= len(garden):
            return True

        if row <= 0:
            return True

        common_point = self.__find_common_point(line)
        left_up_field = garden[row - 1][common_point.j - 1]
        right_up_field = garden[row - 1][common_point.j]

        left_down_field = "^"
        right_down_field = "*"

        if common_point.j + 1 < len(garden[0]):
            left_down_field = garden[row][common_point.j - 1]
            right_down_field = garden[row][common_point.j]

        eventually_print(
            should_print,
            f"{left_up_field} | {right_up_field}\n- - -\n{left_down_field} | {right_down_field}",
        )

        if left_up_field == right_down_field:
            eventually_print(should_print, "[horizontal]: Left up = Right down")
            return False
        elif right_up_field == left_down_field:
            eventually_print(should_print, "[horizontal]: Right up = Left down")
            return False
        else:
            return True

    def is_continuation_in_garden(self, garden, line: "Line", should_print):
        eventually_print(should_print, f"Checking continuation for {self} and {line}")
        if (
            self.is_horizontal()
            and line.is_horizontal()
            and self.__have_common_point(line)
        ):
            result = self.is_continuation_in_garden_horizontal(
                garden, line, should_print
            )
            eventually_print(
                should_print,
                f"Horizontal continuation {self} -> {line} is {result}",
            )
            return result

        if self.is_vertical() and line.is_vertical() and self.__have_common_point(line):
            result = self.is_continuation_in_garden_vertical(garden, line, should_print)
            eventually_print(
                should_print,
                f"Vertical continuation {self} -> {line} is {result}",
            )
            return result

        return False


# endregion


def save_garden_to_file(garden, filename):
    with open(filename, "w") as file:
        for row in garden:
            file.write("".join(row) + "\n")


def pprint(garden):
    for row in garden:
        print(" ".join(row))
    print()


def visit_region(garden: List[List[str]], lines: Set[Line], x, y):
    current = garden[x][y]
    if current == VISITED:
        return 0

    garden[x][y] = VISITED
    area = 1

    # up
    if x - 1 >= 0 and garden[x - 1][y] == current:
        area += visit_region(garden, lines, x - 1, y)

    if x - 1 < 0 or (garden[x - 1][y] != current and garden[x - 1][y] != VISITED):
        lines.add(Line(Point(x, y), Point(x, y + 1)))

    # down
    if x + 1 < len(garden) and garden[x + 1][y] == current:
        area += visit_region(garden, lines, x + 1, y)

    if x + 1 >= len(garden) or (
        garden[x + 1][y] != current and garden[x + 1][y] != VISITED
    ):
        lines.add(Line(Point(x + 1, y), Point(x + 1, y + 1)))

    # left
    if y - 1 >= 0 and garden[x][y - 1] == current:
        area += visit_region(garden, lines, x, y - 1)

    if y - 1 < 0 or (garden[x][y - 1] != current and garden[x][y - 1] != VISITED):
        lines.add(Line(Point(x, y), Point(x + 1, y)))

    # right
    if y + 1 < len(garden[0]) and garden[x][y + 1] == current:
        area += visit_region(garden, lines, x, y + 1)

    if y + 1 >= len(garden[0]) or (
        garden[x][y + 1] != current and garden[x][y + 1] != VISITED
    ):
        lines.add(Line(Point(x, y + 1), Point(x + 1, y + 1)))

    return area


def find_all_visited(garden_a, garden_b):
    new_garden = copy.deepcopy(garden_a)

    for i in range(len(garden_a)):
        for j in range(len(garden_a[0])):
            if garden_b[i][j] == VISITED:
                new_garden[i][j] = VISITED

    return new_garden


# region COUNT_SIDES
def count_vertical_sides(garden, lines: List[Line], should_print):
    vertical_lines = [line for line in lines if line.is_vertical()]
    vertical_lines = sorted(vertical_lines, key=lambda x: (x.point1.j, x.point1.i))
    same_column: Dict[int, List[Line]] = {}
    for line in vertical_lines:
        if line.point1.j not in same_column:
            same_column[line.point1.j] = []
        same_column[line.point1.j].append(line)

    sides_count = len(same_column.keys())
    for column in same_column.values():
        sorted(column, key=lambda x: (x.point1.j, x.point1.i))
        for i in range(len(column) - 1):
            if not column[i].is_continuation_in_garden(
                garden, column[i + 1], should_print
            ):
                sides_count += 1
            eventually_print(
                should_print,
                f"\n\n",
            )

    return sides_count


def count_horizontal_sides(garden, lines: List[Line], should_print):
    horizontal_lines = [line for line in lines if line.is_horizontal()]
    horizontal_lines = sorted(horizontal_lines, key=lambda x: (x.point1.i, x.point1.j))
    same_row = {}
    for line in horizontal_lines:
        if line.point1.i not in same_row:
            same_row[line.point1.i] = []
        same_row[line.point1.i].append(line)

    sides_count = len(same_row.keys())
    for row in same_row.values():
        sorted(row, key=lambda x: x.point1.j)
        for i in range(len(row) - 1):
            if not row[i].is_continuation_in_garden(garden, row[i + 1], should_print):
                sides_count += 1

            eventually_print(
                should_print,
                "\n\n",
            )

    return sides_count


# endregion


def count_sides(garden, lines: List[Line], should_print):
    horizontal = count_horizontal_sides(garden, lines, should_print)
    vertical = count_vertical_sides(garden, lines, should_print)
    eventually_print(should_print, f"Horizontal = {horizontal}, Vertical = {vertical}")
    return horizontal + vertical


if __name__ == "__main__":
    garden = []

    with open("final_input.txt") as file:
        lines = file.read().splitlines()
        for line in lines:
            garden.append([c for c in line])

    visited_garden = copy.deepcopy(garden)
    working_garden = copy.deepcopy(garden)
    result = 0

    should_print = lambda letter: False

    print("Initial garden size: I = {}, J = {}".format(len(garden), len(garden[0])))
    for i in range(len(garden)):
        for j in range(len(garden[0])):
            if visited_garden[i][j] != VISITED:
                lines = set()
                letter = garden[i][j]
                working_garden = copy.deepcopy(garden)
                ar = visit_region(working_garden, lines, i, j)
                sides = count_sides(working_garden, lines, should_print(letter))

                tmp_result = ar * sides
                print(
                    f"Garden {letter}, result sides = {sides}, result area {ar}, price = {tmp_result}"
                )
                result += tmp_result
                visited_garden = find_all_visited(visited_garden, working_garden)
                if should_print(letter):
                    pprint(working_garden)

    save_garden_to_file(visited_garden, "visited.txt")
    print(f"Result = {result}")
