from itertools import combinations, product

from pyqubo import Binary, Constraint

from quantumglare.common.graph import (
    get_vertices, get_edges_out_for_vertex, get_edges_in_for_vertex,
    get_edges_for_vertex
)


def _get_penalty_constants(edges: list, epsilon: float) -> dict:
    """Get penalty constants for the configuration defined by the edges in the
    input graph.

    :param edges: edges defining the input graph
    :param epsilon: small number used for the penalties

    :return: penalty constant

    """
    vertices = get_vertices(edges)
    penalty_constants = {}

    for v in vertices:
        # max one out
        edges_out = get_edges_out_for_vertex(edges, v)
        n_out = len(edges_out)
        a_v = (1 + epsilon) if n_out > 1 else 0

        # max one in
        edges_in = get_edges_in_for_vertex(edges, v)
        n_in = len(edges_in)
        b_v = (1 + epsilon) if n_in > 1 else 0

        # cycle length at least three
        c = (2 + epsilon)

        penalty_constants[v] = [a_v, b_v, c]

    return penalty_constants


def _get_cost(edges: list, epsilon: float = 0.01):
    """Get the cost associated to the input graph.

    :param edges:  edges defining the input graph
    :param epsilon: small number used for the penalties

    :return: the corresponding cost

    """
    vertices = get_vertices(edges)
    cost = 0

    for edge in edges:
        cost += - Binary(str(tuple(edge))) ** 2

    penalty_constants = _get_penalty_constants(edges, epsilon)

    constraint_one_out = 0
    constraint_one_in = 0
    constraint_min_three = 0
    for v in vertices:
        # max one out
        edges_out_v = get_edges_out_for_vertex(edges, v)
        edges_out_v_pairs = [tuple(c) for c in combinations(edges_out_v, 2)]
        cross_products_out = sum([
            Binary(str((e[0]))) * Binary(str((e[1])))
            for e in edges_out_v_pairs
        ])
        if cross_products_out:
            constraint_one_out += penalty_constants[v][0] * Constraint(
                cross_products_out, label=f'one out for vertex: {v}'
            )

        # max one in
        edges_in_v = get_edges_in_for_vertex(edges, v)
        edges_in_v_pairs = [tuple(c) for c in combinations(edges_in_v, 2)]
        cross_products_in = sum([
            Binary(str((e[0]))) * Binary(str((e[1])))
            for e in edges_in_v_pairs
        ])
        if cross_products_in:
            constraint_one_in += penalty_constants[v][1] * Constraint(
                cross_products_in, label=f'one in for vertex: {v}'
            )

        edges_v = get_edges_for_vertex(edges, v)
        edges_v_pairs = [tuple(c) for c in combinations(edges_v, 2)]
        # cycle length at least three
        cross_products_length_2_cycles = sum([
            Binary(str((e[0]))) * Binary(str((e[1])))
            for e in edges_v_pairs
            if e[0][0] == e[1][1] and e[0][1] == e[1][0]
        ])
        if cross_products_length_2_cycles:
            # the factor 0.5 is to avoid double counting as each pair will be
            # present twice as we are looping through the vertices
            constraint_min_three += 0.5 * penalty_constants[v][2] * Constraint(
                cross_products_length_2_cycles,
                label=f'min three cycle length for vertex: {v}'
            )

    cost += constraint_one_out
    cost += constraint_one_in
    cost += constraint_min_three

    return cost


def _cost_to_qubo(cost) -> dict:
    """Get the the Q matrix corresponding to the given cost.

    :param cost: cost

    :return: QUBO matrix

    """
    model = cost.compile()
    Q = model.to_qubo()[0]
    return Q


def get_Q(edges: list) -> dict:
    """Transform the input edges into a QUBO problem defined by Q.

    :param edges: edges of the input graph

    :return: QUBO matrix

    """
    cost = _get_cost(edges)
    Q = _cost_to_qubo(cost)
    return Q


def calculate_energy_for_state(Q: dict, state: list) -> float:
    """Calculate the energy of a state for the QUBO problem defined by Q.

    :param Q: QUBO matrix
    :param state: a state

    :return: energy

    """
    energy = 0
    state_str = [str(edge) for edge in state]

    for k in product(state_str, state_str):
        if k in Q.keys():
            energy += Q[k]

    return energy
