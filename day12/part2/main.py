import copy
from typing import List, Set

VISITED = "$"


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
            return (
                self.point2 == line.point1
                or self.point1 == line.point2
                or self.point1 == line.point1
                or self.point2 == line.point2
            )
        if self.is_vertical() and line.is_vertical():
            return (
                self.point2 == line.point1
                or self.point1 == line.point2
                or self.point1 == line.point1
                or self.point2 == line.point2
            )

        return False

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


class Side:

    def __init__(self, line_1: Line, line_2: Line):
        self.points = set()
        self.points.add(line_1.point1)
        self.points.add(line_1.point2)
        self.points.add(line_2.point1)
        self.points.add(line_2.point2)

    def add_line(self, line: Line):
        self.points.add(line.point1)
        self.points.add(line.point2)

    def is_vertical(self):
        return self.points[0].j == self.points[1].j

    def is_horizontal(self):
        return self.points[0].i == self.points[1].i

    def is_continuation(self, line: Line):
        if self.is_horizontal() and line.is_horizontal():
            return (
                line.point1.i == self.points[0].i and line.point2.i == self.points[1].i
            )
        if self.is_vertical() and line.is_vertical():
            return (
                self.points[0] == line.point1
                or self.points[1] == line.point2
                or self.points[0] == line.point2
                or self.points[1] == line.point1
            )

        return False

    def __str__(self):
        return f"Side({self.points})"


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


def count_sides(lines: List[Line]):
    side_counter = 0

    vertical_lines = [line for line in lines if line.is_vertical()]
    horizontal_lines = [line for line in lines if line.is_horizontal()]

    print(f"Vertical lines: {vertical_lines}")
    print(f"Horizontal lines: {horizontal_lines}")

    vertical_lines = sorted(vertical_lines, key=lambda x: (x.point1.i, x.point1.j))
    horizontal_lines = sorted(horizontal_lines, key=lambda x: (x.point1.j, x.point1.i))

    sides = []

    for i in range(len(vertical_lines)):
        print(f"Vertical line: {vertical_lines[i]} of {len(vertical_lines)}")
        if vertical_lines[i].is_side:
            continue
        no_continuation = True
        
        append = False
        append_index = -1
        for j in range(len(sides)):
            for k in range(len(sides[j])):
                if sides[j][k].is_continuation(vertical_lines[i]):
                    append = True
                    vertical_lines[i].set_is_side()
                    no_continuation = False
                    append_index = j
                    break
            if append:
                break
        if append:
            sides[append_index].append(vertical_lines[i])

        if no_continuation is False:
            continue

        for j in range(i + 1, len(vertical_lines)):
            
            if vertical_lines[i].is_continuation(vertical_lines[j]):
                vertical_lines[i].set_is_side()
                vertical_lines[j].set_is_side()
                sides.append([vertical_lines[i], vertical_lines[j]])
                no_continuation = False
        if no_continuation:
            side_counter += 1
    
    print(f"Sides vertical: {sides}")
    sides = []
    for i in range(len(horizontal_lines)):
        if horizontal_lines[i].is_side:
            continue
        no_continuation = True
        append = False
        append_index = -1
        for j in range(len(sides)):
            for k in range(len(sides[j])):
                if sides[j][k].is_continuation(horizontal_lines[i]):
                    append = True
                    horizontal_lines[i].set_is_side()
                    no_continuation = False
                    append_index = j
                    break
            if append:
                break
        
        if append:
            sides[append_index].append(horizontal_lines[i])
        if no_continuation is False:
            continue
        
        for j in range(i + 1, len(horizontal_lines)):
            if horizontal_lines[i].is_continuation(horizontal_lines[j]):
                if not horizontal_lines[i].is_side:
                    side_counter += 1
                horizontal_lines[i].set_is_side()
                horizontal_lines[j].set_is_side()
                sides.append([horizontal_lines[i], horizontal_lines[j]])
                no_continuation = False
        
        if no_continuation:
            side_counter += 1
    
    print(f"Sides horizontal: {sides}")
    return side_counter


if __name__ == "__main__":
    garden = []

    with open("input.txt") as file:
        lines = file.read().splitlines()
        for line in lines:
            garden.append([c for c in line])

    visited_garden = copy.deepcopy(garden)
    working_garden = copy.deepcopy(garden)
    result = 0

    for i in range(len(garden)):
        for j in range(len(garden[0])):
            if visited_garden[i][j] != VISITED:
                lines = set()
                letter = garden[i][j]
                working_garden = copy.deepcopy(garden)
                ar = visit_region(working_garden, lines, i, j)
                sides = count_sides(lines)
                print(f"Letter {letter}, area = {ar}")
                print(f"Sides = {sides}")
                for indx, line in enumerate(lines, 0):
                    print(f"\t\t{indx + 1}", line)

                tmp_result = ar * sides
                print(
                    f"Garden {letter}, result sides = {sides}, result area {ar}, price = {tmp_result}"
                )
                result += tmp_result
                visited_garden = find_all_visited(visited_garden, working_garden)
                # pprint(visited_garden)

    save_garden_to_file(visited_garden, "visited.txt")
