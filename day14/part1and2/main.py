import copy
import time
from typing import List


def read_point(line: str) -> "Point":
    raw_x, y = line.split(",")
    x = raw_x.replace("p=", "").replace("v=", "")
    return Point(int(x), int(y))


def get_input(file_path: str) -> List["Robot"]:
    with open(file_path, "r") as file:
        lines = file.readlines()
    robots = []
    for line in lines:
        point, velocity = line.split(" ")
        p = read_point(point)
        v = read_point(velocity)
        robots.append(Robot(p, v))
    return robots


class Point:

    def __init__(self, x, y, type="Point"):
        self.x = x
        self.y = y
        self.type = type

    def __str__(self):
        return f"{self.type}({self.x}, {self.y})"


class Boundaries(Point):

    def __init__(self, x, y):
        super().__init__(x, y, "Boundaries")


class Velocity(Point):

    def __init__(self, x, y):
        super().__init__(x, y, "Velocity")


class Robot:

    def __init__(self, point: "Point", velocity: "Point"):
        self.point = point
        self.velocity = Velocity(velocity.x, velocity.y)

    def move(self, boundaries: "Boundaries"):
        self.point.x = calc_new_position(self.point.x, self.velocity.x, boundaries.x)
        self.point.y = calc_new_position(self.point.y, self.velocity.y, boundaries.y)

    def __str__(self):
        return f"Robot( {self.point}, {self.velocity} )"


def calc_new_position(current_position: int, velocity: int, limit: int) -> int:
    return (current_position + velocity) % limit


def calc_safety_area(room) -> int:
    return sum([sum(row) for row in room])


def print_room(room):
    tmp = copy.deepcopy(room)
    for i in range(len(tmp)):
        for j in range(len(tmp[i])):
            if tmp[i][j] == 0:
                tmp[i][j] = "."

    for row in tmp:
        print(" ".join(map(str, row)))


def splint_2d_in_quadrants(room):
    x = len(room[0]) // 2
    y = len(room) // 2

    q1 = [row[:x] for row in room[:y]]
    q2 = [row[x + 1 :] for row in room[:y]]
    q3 = [row[:x] for row in room[y + 1 :]]
    q4 = [row[x + 1 :] for row in room[y + 1 :]]
    return [q1, q2, q3, q4]


def save_to_output(room):
    tmp = copy.deepcopy(room)
    for i in range(len(tmp)):
        for j in range(len(tmp[i])):
            if tmp[i][j] == 0:
                tmp[i][j] = "."
            else:
                tmp[i][j] = "#"
    with open("output.txt", "w") as file:
        for row in tmp:
            file.write("".join(map(str, row)) + "\n")

def part1(data, boundaries, seconds):
    room = [[0 for _ in range(boundaries.x)] for _ in range(boundaries.y)]
    for robot in data:
        for _ in range(seconds):
            robot.move(boundaries)
    
    for robot in data:
        room[robot.point.y][robot.point.x] += 1

    print_room(room)
    quadrants = splint_2d_in_quadrants(room)
    print("\n\n")
    safety_factor = 1
    for q in quadrants:
        print_room(q)
        print("\n\n")
        safety_factor *= calc_safety_area(q)
    
    print(f"Safety factor: {safety_factor}")

def has_x_lines_with_y_points_in_row(room, x, y):
    count = 0
    for i in range(len(room)):
        row_count = 0
        for j in range(len(room[i])):
            if room[i][j] != 0:
                row_count += 1
                if row_count == y:
                    count += 1
                    break
            else:
                row_count = 0
        
        if count == x:
            return True


def part2(data, boundaries):
    start_point = 0
    for i in range(1, 10000):
        
        room = [[0 for _ in range(boundaries.x)] for _ in range(boundaries.y)]
        for robot in data:
            robot.move(boundaries)
            room[robot.point.y][robot.point.x] += 1
        if i >= start_point and has_x_lines_with_y_points_in_row(room, 2, 6):
            save_to_output(room)
            print(f"Second: {i}")
            time.sleep(0.2)
        #input("Press Enter to continue...")


if __name__ == "__main__":
    seconds = 100
    boundaries = Boundaries(101, 103)
    data = get_input("input.txt")

    # part1(data, boundaries, seconds)
    part2(data, boundaries)  # 6355
    

    # room = [[0 for _ in range(boundaries.x)] for _ in range(boundaries.y)]
    # for robot in data:
    #     for _ in range(seconds):
    #         robot.move(boundaries)
    
    # for robot in data:
    #     room[robot.point.y][robot.point.x] += 1

    # print_room(room)
    # quadrants = splint_2d_in_quadrants(room)
    # print("\n\n")
    # safety_factor = 1
    # for q in quadrants:
    #     print_room(q)
    #     print("\n\n")
    #     safety_factor *= calc_safety_area(q)
    
    # print(f"Safety factor: {safety_factor}")