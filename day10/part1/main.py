pprint = lambda x: print("\n".join([" ".join([str(y) for y in row]) for row in x]))


class Node:
    legit_hills = set()

    def __init__(self, i, j, level=0, parent=None):
        self.i = i
        self.j = j
        self.level = level
        self.parent = parent
        self.children = []
        self.visited = False

    def add_child(self, i, j):
        self.children.append(Node(i, j, self.level + 1, self))

    def reset(self):
        Node.legit_hills = set()
    
    def result(self):
        return len(Node.legit_hills)
    
    def add_hill(self):
        Node.legit_hills.add((self.i, self.j))

    def has_continuation(self):
        return len(self.children) > 0

    def reached_hill_top(self):
        return self.level == 9

    def is_visited(self):
        return self.visited

    def set_visited(self):
        self.visited = True

    def indexes_str(self):
        return f"({self.i}, {self.j})"

    def go(self, data):
        if self.is_visited():
            return
        self.set_visited()
        next_moves = find_next_moves(data, self.i, self.j)
        if self.reached_hill_top():
            self.add_hill()
            return

        if len(next_moves) == 0:
            return

        for move in next_moves:
            i, j = move
            self.add_child(i, j)

        for next_node in self.children:
            next_node.go(data)

    def __str__(self, level=0):
        ret = "\t" * level + self.indexes_str() + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret


def find_next_moves(data, current_i, current_j):
    moves = []
    current_step = data[current_i][current_j]

    # bottom
    if current_i - 1 >= 0 and data[current_i - 1][current_j] == current_step + 1:
        moves.append((current_i - 1, current_j))

    # top
    if current_i + 1 < len(data) and data[current_i + 1][current_j] == current_step + 1:
        moves.append((current_i + 1, current_j))

    # left
    if current_j - 1 >= 0 and data[current_i][current_j - 1] == current_step + 1:
        moves.append((current_i, current_j - 1))

    # right
    if (
        current_j + 1 < len(data[current_i])
        and data[current_i][current_j + 1] == current_step + 1
    ):
        moves.append((current_i, current_j + 1))

    return moves


if __name__ == "__main__":

    to_int = lambda x: "." if x == "." else int(x)

    data = []
    with open("input.txt") as file:
        for line in file.readlines():
            data.append([to_int(x) for x in line.strip()])

    pprint(data)
    start_points = [
        (i, j) for i in range(len(data)) for j in range(len(data[i])) if data[i][j] == 0
    ]
    
    result = 0
    for i, j in start_points:
        root = Node(i, j)
        root.go(data)
        result += root.result()
        root.reset()


    print(f'Result: {result}')
