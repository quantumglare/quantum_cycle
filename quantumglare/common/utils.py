import os

import numpy as np
import pandas as pd


def convert_list_of_strings_to_list_of_tuples(x: list) -> list:
    """Convert  e.g. ['(12, 5)', '(5, 12)'] to [(12, 5), (5, 12)]

    :param x: list of strings

    :return: list of tuples

    """
    return [tuple(int(s) for s in i[1:-1].split(',')) for i in x]


def comb(n, k):
    """Get the number of combinations for n elements in groups of k elements.

    :param n: total number of elements
    :param k: number of elements per group

    :return: number of combinations

    """
    return np.math.factorial(n)/(np.math.factorial(k)*np.math.factorial(n-k))


def write_output_to_csv(
        data: dict,
        filename: str,
) -> None:
    """
    :param data: data to be written to CSV
    :param filename: filename for the output CSV file

    :return:

    """
    enriched_data = data
    output_df = pd.DataFrame(
        data=enriched_data,
        columns=[
            'tag',
            'n_cycles',
            'cycle_length',
            'n_vertices',
            'p_noise',
            'n_edges_noise',
            'seed_input_graph',
            'seed_embedding',
            'num_reads',
            'anneal_time',
            'pause_duration',
            'pause_start',
            'time_qubo',
            'time_dwave_response',
            'time_overall_computation',
            'solution_frequency',
            'runs_to_solution',
            'input_graph',
            'solutions',
            'dwave_solution_df',
            'embedding_context',
        ]
    )
    output_df.to_csv(
        filename,
        mode='a',
        header=True if not os.path.exists(filename) else False,
        index=False
    )
    return None
