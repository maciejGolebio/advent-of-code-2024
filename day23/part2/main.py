from functools import cache
from typing import Dict, List, Set, Tuple


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


def build_neighbors_map() -> Dict[Node, Set[Node]]:
    all_nodes = get_all_nodes()
    graph = {n: set() for n in all_nodes}

    # Fill in the adjacency sets
    for i in range(len(all_nodes)):
        for j in range(i + 1, len(all_nodes)):
            n1, n2 = all_nodes[i], all_nodes[j]
            if is_connected(n1, n2):
                graph[n1].add(n2)
                graph[n2].add(n1)

    print(graph)
    return graph


def bron_kerbosch_with_pivot(
    R: Set[Node],
    P: Set[Node],
    X: Set[Node],
    graph: Dict[Node, Set[Node]],
    best_clique: List[Node],
) -> None:
    # https://www.youtube.com/watch?v=j_uQChgo72I algorithm explanation
    if not P and not X:
        if len(R) > len(best_clique):
            best_clique.clear()
            best_clique.extend(sorted(R))
        return

    pivot = next(iter(P.union(X)))

    for v in P - graph[pivot]:
        newR = R.union({v})
        newP = P.intersection(graph[v])
        newX = X.intersection(graph[v])

        bron_kerbosch_with_pivot(newR, newP, newX, graph, best_clique)

        P.remove(v)
        X.add(v)


def find_largest_clique() -> List[Node]:
    graph = build_neighbors_map()  # node -> set of neighbors
    all_nodes = set(graph.keys())  # P initially
    best_clique: List[Node] = []
    bron_kerbosch_with_pivot(R=set(), P=all_nodes, X=set(), graph=graph, best_clique=best_clique)

    return best_clique

if __name__ == "__main__":

    # print(pprint(cycles_of_3))
    # print(len(cycles_of_3))
    res = find_largest_clique()
    res.sort()
    print(",".join(res))
    print("-----------------------------")

