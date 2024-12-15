import copy
from main import count_sides, VISITED, find_all_visited, visit_region


def get_input(filename):
    garden = []
    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            garden.append([c for c in line])

    return garden


def test_count_sides_simple_case():
    expected_sequence = [(4, 4), (4, 4), (8, 4), (4, 1), (4, 3)]
    results = []
    garden = get_input("input1.txt")
    visited_garden = copy.deepcopy(garden)
    for i in range(len(garden)):
        for j in range(len(garden[0])):
            if visited_garden[i][j] != VISITED:
                working_garden = copy.deepcopy(garden)
                lines = set()
                ar = visit_region(working_garden, lines, i, j)
                sides = count_sides(working_garden, lines, False)
                results.append((sides, ar))
                visited_garden = find_all_visited(visited_garden, working_garden)

    assert len(results) == len(expected_sequence)
    for i in range(len(results)):
        print(f"Comparing {results[i]} with {expected_sequence[i]}")
        assert results[i][0] == expected_sequence[i][0]
        assert results[i][1] == expected_sequence[i][1]
        assert results[i] == expected_sequence[i]


def test_count_sides_E_shape_case():
    expected_sequence = [(12, 17), (4, 4), (4, 4)]
    results = []
    garden = get_input("input2.txt")
    visited_garden = copy.deepcopy(garden)
    for i in range(len(garden)):
        for j in range(len(garden[0])):
            if visited_garden[i][j] != VISITED:
                working_garden = copy.deepcopy(garden)
                lines = set()
                ar = visit_region(working_garden, lines, i, j)
                sides = count_sides(working_garden, lines, False)
                results.append((sides, ar))
                visited_garden = find_all_visited(visited_garden, working_garden)

    assert len(results) == len(expected_sequence)
    for i in range(len(results)):
        print(f"Comparing {results[i]} with {expected_sequence[i]}")
        assert results[i][0] == expected_sequence[i][0]
        assert results[i][1] == expected_sequence[i][1]
        assert results[i] == expected_sequence[i]


def test_count_sides_AB_case():
    expected_sequence = [(12, 28), (4, 4), (4, 4)]
    results = []
    garden = get_input("input3.txt")
    visited_garden = copy.deepcopy(garden)
    for i in range(len(garden)):
        for j in range(len(garden[0])):
            if visited_garden[i][j] != VISITED:
                working_garden = copy.deepcopy(garden)
                lines = set()
                ar = visit_region(working_garden, lines, i, j)
                sides = count_sides(working_garden, lines, False)
                results.append((sides, ar))
                visited_garden = find_all_visited(visited_garden, working_garden)

    assert len(results) == len(expected_sequence)
    for i in range(len(results)):
        print(f"Comparing {results[i]} with {expected_sequence[i]}")
        assert results[i][0] == expected_sequence[i][0]
        assert results[i][1] == expected_sequence[i][1]
        assert results[i] == expected_sequence[i]


def test_count_sides_larger_case():
    expected_sequence = [
        (10, 12),
        (4, 4),
        (22, 14),
        (12, 10),
        (10, 13),
        (12, 11),
        (4, 1),
        (8, 13),
        (16, 14),
        (6, 5),
        (6, 3),
    ]
    results = []
    garden = get_input("input4.txt")
    visited_garden = copy.deepcopy(garden)
    for i in range(len(garden)):
        for j in range(len(garden[0])):
            if visited_garden[i][j] != VISITED:
                working_garden = copy.deepcopy(garden)
                lines = set()
                ar = visit_region(working_garden, lines, i, j)
                sides = count_sides(working_garden, lines, False)
                results.append((sides, ar))
                visited_garden = find_all_visited(visited_garden, working_garden)
    
    assert len(results) == len(expected_sequence)
    for i in range(len(results)):
        print(f"Comparing {results[i]} with {expected_sequence[i]}")
        assert results[i][0] == expected_sequence[i][0]
        assert results[i][1] == expected_sequence[i][1]
        assert results[i] == expected_sequence[i]
