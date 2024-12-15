from typing import List


class Point:

    def __init__(self, x, y, type="Button"):
        self.x = x
        self.y = y
        self.type = type

    def __str__(self):
        return f"{self.type}: {self.x}, {self.y}"


class ClawMachine:
    def __init__(self, a: Point, b: Point, prize: Point):
        self.a = a
        self.b = b
        self.prize = prize


def button_line_to_point(line: str) -> Point:
    splitted = line.split(",")
    left = splitted[0].replace("Button A: X+", "").replace("Button B: X+", "")
    right = splitted[1].replace(" Y+", "")
    return Point(int(left), int(right))


def prize_line_to_point(line: str) -> Point:
    move = 10000000000000  # 0 for part1
    splitted = line.split(",")
    left = splitted[0].replace("Prize: X=", "")
    right = splitted[1].replace(" Y=", "")
    return Point(int(left) + move, int(right) + move, "Prize")


def get_input() -> List[ClawMachine]:
    claw_machines = []
    with open("input.txt") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 4):
            a = button_line_to_point(lines[i])
            b = button_line_to_point(lines[i + 1])
            prize = prize_line_to_point(lines[i + 2])
            claw_machines.append(ClawMachine(a, b, prize))
    return claw_machines


def calc_b_times(claw: ClawMachine) -> int:
    return ((claw.prize.y * claw.a.x) - (claw.a.y * claw.prize.x)) / (
        (claw.a.x * claw.b.y) - (claw.a.y * claw.b.x)
    )


def calc_a_times(claw: ClawMachine, a_times) -> int:
    return (claw.prize.x - claw.b.x * a_times) / claw.a.x


def is_legit_result(times: float):
    return times.is_integer() and times >= 0  # uncomment for part1 and times <= 100


price_formula = lambda a, b: int(a * 3 + b)

if __name__ == "__main__":
    games = get_input()
    summed_price = 0
    for game in games:
        b_times = calc_b_times(game)
        a_times = calc_a_times(game, b_times)
        if is_legit_result(a_times) and is_legit_result(b_times):
            price = price_formula(a_times, b_times)
            summed_price += price
            print(
                f"Game: {game.prize.type} A = {a_times}, B = {b_times}, Price = {price}"
            )

        else:
            print(f"Game: {game.prize.type} A = {a_times}, B = {b_times}")
    print(f"Summed price: {summed_price}")
