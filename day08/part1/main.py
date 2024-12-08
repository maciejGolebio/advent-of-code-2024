
def pretty_print_map(city_map):
    for line in city_map:
        print("".join(line))

def get_directional_distance_move(a, b):
    return a[0] - b[0], a[1] - b[1]

def find_points_on_line_with_distance(starting_point, i_move, j_move):
    points = []
    i = starting_point[0]
    j = starting_point[1]

    points.append((i + i_move, j+  j_move))
    points.append((i - i_move, j - j_move))

    return points

    
def find_antinodes_for_pair(max_i, max_y, antenna_a, antenna_b, anti_nodes):
    i_move, j_move = get_directional_distance_move(antenna_a, antenna_b)

    print(f'Move: i={i_move}, j={j_move}')
    points_a = find_points_on_line_with_distance(antenna_a, i_move, j_move)
    points_b = find_points_on_line_with_distance(antenna_b, i_move, j_move)
    points = points_a + points_b
    for p in points:
        if p[0] < 0 or p[1] < 0 or p[0] >= max_i or p[1] >= max_y:
            print("Out of bounds, antenna_a: ", antenna_a, " antenna_b: ", antenna_b, " point: ", p)
            continue
        if p == antenna_a or p == antenna_b:
            print("Antenna point, antenna_a: ", antenna_a, " antenna_b: ", antenna_b, " point: ", p)
            continue
        print('For antenna_a: ', antenna_a, ' antenna_b: ', antenna_b, ' point: ', p)
        anti_nodes.add(p)


def find_points_permutations(antennas):
    permutations = []
    for i in range(len(antennas)):
        for j in range(i+1, len(antennas)):
            permutations.append((antennas[i], antennas[j]))
            
    return permutations
    



if __name__ == "__main__":
    city_map = []
    with open("input.txt") as file:
        for line in file:
            city_map.append([x for x in line.strip()])
            
    antennas = {}
    chars = set()
    anti_nodes = set()
    for i in range(len(city_map)):
        for j in range(len(city_map[i])):
            if city_map[i][j] != "." and city_map[i][j] != "#":
                if city_map[i][j] not in antennas:
                   antennas[city_map[i][j]] = [(i, j)]
                else:
                    antennas[city_map[i][j]].append((i, j)) 
                chars.add(city_map[i][j])

    
    for char in chars:
        perms = find_points_permutations(antennas[char])
        for a, b in perms:
            find_antinodes_for_pair(len(city_map), len(city_map[0]), a, b, anti_nodes)

    print(len(anti_nodes))