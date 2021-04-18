import os
import numpy as np

from quantumglare.solvers import quantum_solver
from quantumglare.common import graph, utils


def generate_raw_data(
        n_cycles: int,
        cycle_length: int,
        p_noise: float = None,
        n_edges_noise: int = None,
        seeds_embedding=list(range(0, 50)),
        seed_input_graph: int = None,
        tag_prefix='',
):
    """Generate raw output data obtained from the quantum annealer for the
    input problem and parameters specified. The data are written in the
    specified file.

    :param n_cycles: number of cycles
    :param cycle_length: cycle length of each cycle
    :param p_noise: fraction of noise edges added
    :param n_edges_noise: number of noise edges added
    :param seeds_embedding: start values for the random seeds used for
    generation of the embedding
    :param seed_input_graph: seed for the input graph
    :param tag_prefix: prefix for the tag

    :return: None

    """
    if p_noise is None and n_edges_noise is None:
        raise Exception(
            'At least one between p_noise and n_edges_noise must be set'
        )
    if p_noise is not None and n_edges_noise is not None:
        raise Exception(
            'Only one between p_noise and n_edges_noise must be set'
        )

    n_vertices = n_cycles * cycle_length
    if p_noise is not None:
        n_edges_noise = int(np.round(p_noise * n_vertices * (n_vertices - 2)))

    tag = tag_prefix + f"n_cycles_{n_cycles}_cycle_length_{cycle_length}" \
                       f"_n_edges_noise_{n_edges_noise}"

    graph_hamiltonian_cycles = graph.create_graph_hamiltonian_cycles(
        n_cycles=n_cycles, cycle_length=cycle_length
    )

    if seed_input_graph is not None:
        seeds_input_graph = [seed_input_graph] * len(seeds_embedding)
    else:
        seeds_input_graph = seeds_embedding

    for seed_e, seed_ig in zip(seeds_embedding, seeds_input_graph):
        params = {
            'tag': tag,
            'seed_input_graph': seed_ig,
            'seed_embedding': seed_e,
            'n_cycles': n_cycles,
            'cycle_length': cycle_length,
            'n_vertices': n_vertices,
            'p_noise': p_noise,
            'n_edges_noise': n_edges_noise,
            'anneal_time': 200,
            'num_reads': 100,
            'pause_duration': 100,
            'pause_start': 0.4,
        }
        print(f"\n====== n_cycles: {n_cycles}, cycle_length: {cycle_length}, "
              f"n_edges_noise: {n_edges_noise}, seed_embedding: {seed_e}, "
              f"seed_input_graph: {seed_ig} ======")
        input_graph = graph.add_noise(
            graph_hamiltonian_cycles, n_edges_noise, seed_ig
        )
        output = quantum_solver.solve(
            input_graph=input_graph,
            params=params,
        )
        filename = os.path.join('data', 'raw_data.csv')
        utils.write_output_to_csv(data=output, filename=filename)
    return None


def main():
    seeds_embedding = list(range(0, 2))

    # Note that for a Dwave Advantage processor with 5436 qubits,
    # the theoretical maximum for zero noise is 1359 (using cycles of length 4)
    # generate data for Fig 3a - different p_noise
    n_cycles_list = [15, 150, 300, 450, 600, 750, 900, 1050, 1200, 1350]
    for n_cycles in n_cycles_list:
        generate_raw_data(
            n_cycles=n_cycles,
            cycle_length=4,
            p_noise=0,
            seeds_embedding=seeds_embedding,
        )

    n_cycles_list = [150, 300, 450, 600, 750, 900, 1050]
    for n_cycles in n_cycles_list:
        generate_raw_data(
            n_cycles=n_cycles,
            cycle_length=4,
            p_noise=5e-5,
            seeds_embedding=seeds_embedding,
        )

    n_cycles_list = [150, 300, 450, 600, 750, 900]
    for n_cycles in n_cycles_list:
        generate_raw_data(
            n_cycles=n_cycles,
            cycle_length=4,
            p_noise=1e-4,
            seeds_embedding=seeds_embedding,
        )

    # generate additional data for Fig 3b - different cycle_length
    n_cycles_list = [20, 200, 400, 600, 800, 1000, 1200, 1400]
    for n_cycles in n_cycles_list:
        generate_raw_data(
            n_cycles=n_cycles,
            cycle_length=3,
            p_noise=5e-5,
            seeds_embedding=seeds_embedding,
        )

    n_cycles_list = [12, 120, 240, 360, 480, 600, 720, 840]
    for n_cycles in n_cycles_list:
        generate_raw_data(
            n_cycles=n_cycles,
            cycle_length=5,
            p_noise=5e-5,
            seeds_embedding=seeds_embedding,
        )

    # generate data for Fig 4 - different Nv
    n_edges_noise_list = [0, 100, 200, 300, 400, 500, 600]
    for n_edges_noise in n_edges_noise_list:
        generate_raw_data(
            n_cycles=250,
            cycle_length=4,
            n_edges_noise=n_edges_noise,
            seeds_embedding=seeds_embedding,
        )

    n_edges_noise_list = [
        0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200
    ]
    for n_edges_noise in n_edges_noise_list:
        generate_raw_data(
            n_cycles=1000,
            cycle_length=4,
            n_edges_noise=n_edges_noise,
            seeds_embedding=seeds_embedding,
        )


if __name__ == '__main__':
    main()
