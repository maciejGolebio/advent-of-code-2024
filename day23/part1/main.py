from functools import cache
from typing import List, Tuple


def pprint(cycles):
    return "\n".join([to_cycle_string(cycle) for cycle in cycles])


Node = str
Edge = Tuple[Node, Node]
edges = []

with open("input.txt") as f:
    for line in f.readlines():
        l = line.strip().split("-")
        l.sort()
        edges.append(tuple(l))


@cache
def nodes_to_edge(node1: Node, node2: Node) -> Edge:
    edge = [node1, node2]
    edge.sort()
    return tuple(edge)


@cache
def get_all_nodes() -> List[Node]:
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])
        nodes.add(edge[1])
    return list(nodes)


@cache
def get_all_edges_for_node(node: Node) -> List[Edge]:
    return [edge for edge in edges if node in edge]


@cache
def next_node(node: Node, edge: Edge) -> Node:
    return edge[0] if edge[1] == node else edge[1]


@cache
def is_connected(node1: Node, node2: Node) -> bool:
    return nodes_to_edge(node1, node2) in edges


def to_cycle_string(cycle: List[Node]) -> str:
    cycle.sort()
    return "-".join(cycle)


@cache
def to_cycle_str_of_3(node1: Node, node2: Node, node3: Node) -> str:
    return to_cycle_string([node1, node2, node3])


@cache
def to_cycle_list(cycle: str) -> List[Node]:
    return cycle.split("-")


def find_all_connected_closed_n_nodes(n=3) -> List[List[Node]]:
    visited = set()
    connected = []

    def dfs(node: Node, n: int, path: List[Node] = []) -> List[List[Node]]:
        cycles = set()
        if n == 1 and is_connected(node, path[0]):
            return [to_cycle_string(path)]

        elif n == 1:
            return []

        for edge in get_all_edges_for_node(node):
            next = next_node(node, edge)
            if next not in visited and is_connected(node, next):
                cycles.update(dfs(next, n - 1, path + [next]))

        return cycles

    for node in get_all_nodes():
        visited.add(node)
        connected.extend(dfs(node, n, [node]))

    return [to_cycle_list(cycle) for cycle in connected]


map_node_to_t_contains = lambda node: node[0] == "t"


def filter_cycles(cycles: List[List[Node]]) -> List[List[str]]:
    return [cycle for cycle in cycles if any(map(map_node_to_t_contains, cycle))]


if __name__ == "__main__":
    cycles_of_3 = find_all_connected_closed_n_nodes(3)
    #print(pprint(cycles_of_3))
    #print(len(cycles_of_3))
    print(len(find_all_connected_closed_n_nodes(6)))
    print("-----------------------------")
    #filtered = filter_cycles(cycles_of_3)
    #print(pprint(filtered))
    #print(len(filtered))
