import copy

VISITED = "$"


def save_garden(garden, filename):
    with open(filename, "w") as file:
        for row in garden:
            file.write("".join(row) + "\n")


def pprint(garden):
    for row in garden:
        print(" ".join(row))
    print()


def visit_region(garden, x, y):
    current = garden[x][y]
    if current == VISITED:
        return 0, 0
    garden[x][y] = VISITED
    
    perimeter = 0
    area = 1

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (
                x + i >= 0
                and x + i < len(garden)
                and y + j >= 0
                and y + j < len(garden[0])
                
                # not diagonals
                and (i == 0 or j == 0)
            ):
                # print(f"({x + i}, {y + j}) = {garden[x + i][y + j]}")
                if garden[x + i][y + j] == current:
                    per, ar = visit_region(garden, x + i, y + j)
                    perimeter += per
                    area += ar

                if (
                    garden[x + i][y + j] != current
                    and garden[x + i][y + j] != VISITED
                    and (i == 0 or j == 0)
                ):
                    perimeter += 1
                    # print(
                    #     f"Border between {current} y:{i} x:{j}  |  {garden[x + i][y + j]} y:{x + i} x:{y + j}"
                    # )

            elif i == 0 or j == 0:
                perimeter += 1
                # print(f"Border between {current} y:{i} x:{j}  |  Outside")

    return perimeter, area


def find_all_visited(garden_a, garden_b):
    new_garden = copy.deepcopy(garden_a)

    for i in range(len(garden_a)):
        for j in range(len(garden_a[0])):
            if garden_b[i][j] == VISITED:
                new_garden[i][j] = VISITED

    return new_garden


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

                letter = garden[i][j]
                working_garden = copy.deepcopy(garden)
                per, ar = visit_region(working_garden, i, j)

                print(f"Garden {letter} result = {(per, ar)}")
                tmp_result = per * ar
                result += tmp_result
                visited_garden = find_all_visited(visited_garden, working_garden)

    print(result)

    # save_garden(visited_garden, "visited.txt")
