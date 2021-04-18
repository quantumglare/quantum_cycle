from itertools import permutations
import random


def is_valid(edges_output: list, edges_input: list) -> bool:
    """Check if edges_output is a partition of edges_input into Hamiltonian
    cycles of length of 3 or more.

    :param edges_input: edges defining the original graph
    :param edges_output: subset of edges_input returned by the algorithm used
    to find a partition of edges_input into Hamiltonian cycles of length of 3
    or more.

    :return: True if edges_output is a partition of edges_input into
    Hamiltonian cycles of length of 3 or more, False otherwise.

    """
    vertices_input = get_vertices(edges_input)
    vertices_output = get_vertices(edges_output)
    if set(vertices_input) != set(vertices_output):
        return False

    vertices = vertices_output
    edges = edges_output
    while True:
        vertices_cycle = []
        edges_cycle = []
        u_start = random.choice(vertices)
        u_from = u_start
        while True:
            edges_u_from = [edge for edge in edges if edge[0] == u_from]
            # if there is not exactly one edge the output is not a solution
            if len(edges_u_from) != 1:
                return False
            vertices_cycle += [u_from]
            edges_cycle += edges_u_from
            u_to = edges_u_from[0][1]
            # if we went through all the edges but the path does not close the
            # output is not a solution
            if all([
                u_to != u_start,
                len(edges_cycle) == len(edges) or (u_to in vertices_cycle)
            ]):
                return False
            if u_to == u_start:
                break
            u_from = u_to
        if len(vertices_cycle) == 2:
            return False
        vertices = [v for v in vertices if v not in vertices_cycle]
        edges = [e for e in edges if e not in edges_cycle]

        if len(edges) == 0 and len(vertices) == 0:
            return True


def get_vertex_permutations(vertices: list) -> list:
    """Get all the permutations of input vertices arranged in pairs

    :param vertices: vertices in the graph

    :return: permutations

    """
    vertex_permutations = [tuple(p) for p in permutations(vertices, 2)]
    return vertex_permutations


def get_vertices(edges: list) -> list:
    """Get all the vertices belonging to input edges

    :param edges: edges in the graph

    :return: vertices

    """
    edges_list_of_tuples = [list(e) for e in edges]
    return list(set(sum(edges_list_of_tuples, [])))


def get_edges_for_vertex(edges: list, vertex: int) -> list:
    """Get all the edges in the input edges containing the input vertex

    :param edges: edges of the graph
    :param vertex: vertex of which we want to find the corresponding edges

    :return: selected edges

    """
    return [e for e in edges if e[0] == vertex or e[1] == vertex]


def get_edges_out_for_vertex(edges: list, vertex: int) -> list:
    """Get a sublist of edges that have the specified vertex as first element

    :param edges: edges of the graph
    :param vertex: vertex of which we want to find the corresponding edges

    :return: selected edges

    """
    return [e for e in edges if e[0] == vertex]


def get_edges_in_for_vertex(edges: list, vertex: int) -> list:
    """Get a sublist of edges that have the specified vertex as second element

    :param edges: edges of the graph
    :param vertex: vertex of which we want to find the corresponding edges

    :return: selected edges

    """
    return [e for e in edges if e[1] == vertex]


def _create_singe_cycle(start_vertex: int, n_vertices: int) -> list:
    """Create a cycle starting from start_vertex with n_vertices in
    increasing order.

    :param start_vertex: vertex from which to start and end
    :param n_vertices: number of total vertices in output cycle

    :return: the edges forming a cycle

    """
    edges = []
    for v in range(start_vertex, start_vertex + n_vertices - 1):
        edges += [(v, v + 1)]
    edges += [(start_vertex + n_vertices - 1, start_vertex)]
    return edges


def create_graph_hamiltonian_cycles(n_cycles: int, cycle_length: int) -> list:
    """Create a a graph composed of the specified number of hamiltonian cycles
    with the specified cycle length.

    :param n_cycles: number of cycles
    :param cycle_length: length of each cycle

    :return: the edges forming the constructed graph

    """
    edges = []
    for j in range(n_cycles):
        edges += _create_singe_cycle(j * cycle_length, cycle_length)
    return edges


def add_noise(edges: list, n_edges_to_add: int, seed: int) -> list:
    """ Add the specified number of edges connecting the existing vertices of
    the input graph.

    :param edges: list of edges of the input graph
    :param n_edges_to_add: list of edges to be added
    :param seed: seed of random number generator

    :return: the edges forming the graph with added noise

    """
    vertices = get_vertices(edges)
    edges_noise = []

    random.seed(seed)
    while len(edges_noise) < n_edges_to_add:
        vertex_0 = random.choice(vertices)
        other_vertices = list(set(vertices) - {vertex_0})
        vertex_1 = random.choice(other_vertices)
        edge_temp = (vertex_0, vertex_1)
        if edge_temp not in (edges + edges_noise):
            edges_noise += [edge_temp]

    return edges + edges_noise
