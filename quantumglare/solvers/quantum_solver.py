import time
from collections import defaultdict
import json

import pandas as pd
import numpy as np
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import AutoEmbeddingComposite

from quantumglare.common.qubo import get_Q
from quantumglare.common import embedding, graph, utils

from quantumglare import settings  # NOQA


def _get_dwave_response(
        Q: dict,
        num_reads: int,
        anneal_time: int,
        pause_duration: int,
        pause_start: float,
        seed_embedding: int,
) -> pd.DataFrame:
    """Get the response from D-Wave for the problem specified by Q.

    :param Q: QUBO matrix
    :param num_reads: number of times the schedule is run on the quantum
    annealer
    :param anneal_time: time for the annealing part of the schedule
    :param pause_duration: time for the pause part of the schedule
    :param pause_start: value for the s parameter at which the pause starts
    :param seed_embedding: start random seed for the embedding generation

    :return: D-Wave response

    """
    if pause_duration > 0:
        schedule = [
            [0.0, 0.0],
            [pause_start * anneal_time, pause_start],
            [pause_start * anneal_time + pause_duration, pause_start],
            [anneal_time + pause_duration, 1.0]
        ]
    else:
        schedule = [[0.0, 0.0], [anneal_time, 1.0]]

    solver = DWaveSampler()
    sampler = AutoEmbeddingComposite(
        solver,
        find_embedding=embedding.find_embedding,
        embedding_parameters={
            "random_seed": seed_embedding,
            "verbose": 2,
            "interactive": True,
        },
    )
    response = sampler.sample_qubo(
        Q,
        num_reads=num_reads,
        max_answers=num_reads,
        anneal_schedule=schedule,
        answer_mode='histogram',
        return_embedding=True,
    )

    return response


def _extract_states_and_counts(response) -> pd.DataFrame:
    """Convert the response obtained from D-Wave into a DataFrame with energy
    and frequency for the different states.

    :param response: response given by D-Wave

    :return: dataframe with states and frequency

    """
    d = defaultdict(list)
    for (s, e, n, _) in response.data():
        key = str([k for k, v in s.items() if v])
        d[key].append((e, n))
    absfreq = {}
    ens = {}
    for key in d.keys():
        absfreq[key] = np.sum([t[1] for t in d[key]])
        ens[key] = np.mean([t[0] for t in d[key]])
    energy_df = pd.DataFrame.from_dict(ens, orient='index', columns=['energy'])
    freq_df = pd.DataFrame.from_dict(
        absfreq, orient='index', columns=['absolute_frequency']
    )
    results_df_temp = pd.concat([energy_df, freq_df], axis=1)
    results_df_temp.index.name = 'state'
    return results_df_temp.reset_index().sort_values(by='energy')


def get_valid_solutions(states_df: pd.DataFrame, input_graph: list) -> tuple:
    """Get the frequency of valid solution, by summing frequencies of lowest
    energy states in the degenrate case, and outputs all valid solutions
    found.

    :param states_df: dataframe containing the states and energy
    :param input_graph: graph defining the problem to be solved

    :return: a tuple made of:
        - input dataframe with a column added to check if solution is valid
        - frequency of solution
        - all valid solutions

    """
    enriched_states_df = states_df.copy()
    enriched_states_df['is_valid'] = False
    states_df.groupby(by='state')
    lowest_energy = states_df['energy'].min()
    lowest_energy_states_df = states_df[states_df['energy'] == lowest_energy]
    solutions = []
    solution_frequency = 0
    for index, row in lowest_energy_states_df.iterrows():
        edges_solution = utils.convert_list_of_strings_to_list_of_tuples(
            eval(row['state'])
        )
        frequency_temp = row['relative_frequency']
        is_valid = graph.is_valid(edges_solution, input_graph)
        enriched_states_df.loc[
            enriched_states_df['state'] == row['state'], 'is_valid'
        ] = is_valid
        if is_valid:
            solution_frequency += frequency_temp
            solutions.append(edges_solution)
    print(f'number of different solutions: {len(solutions)}')
    return enriched_states_df, solution_frequency, solutions


def solve(input_graph: list, params: dict) -> pd.DataFrame:
    """Find the frequency of valid solutions for a given input graph with
    specified parameters for the solver algorithm.
    When the a solution is present, also outputs the edges defining the
    solution(s).

    :param input_graph: graph defining the problem to be solved
    :param params: parameters to be used by the quantum solver

    :return: dataframe containing the frequency of solution, and the edges
    defining the solution (when a solution is present)

    """
    t0 = time.time()
    Q = get_Q(input_graph)
    t1 = time.time()
    time_qubo = t1-t0
    print(f"Time to get Q: {time_qubo:.2f} s")

    t2 = time.time()
    response = _get_dwave_response(
        Q,
        params['num_reads'],
        params['anneal_time'],
        params['pause_duration'],
        params['pause_start'],
        params['seed_embedding'],
    )
    t3 = time.time()
    time_dwave_response = t3 - t2
    print(f"D-Wave time (including finding embedding): "
          f"{time_dwave_response:.2f} s")
    states_df = _extract_states_and_counts(response)
    states_df['relative_frequency'] = states_df['absolute_frequency'] \
        / params['num_reads']

    enriched_states_df, solution_frequency, edges_solution = \
        get_valid_solutions(states_df, input_graph)
    print(f'the frequency is {solution_frequency:.2%}')
    if 0 < solution_frequency < 1:
        runs_to_solution = np.log(1 - 0.99) / np.log(1 - solution_frequency)
    elif solution_frequency == 1:
        runs_to_solution = 0
    else:
        runs_to_solution = None
    t4 = time.time()
    time_overall_computation = t4 - t0
    print(f"Time to solve overall: {time_overall_computation:.2f} s")
    data = [[
        params['tag'],
        params['n_cycles'],
        params['cycle_length'],
        params['n_vertices'],
        params['p_noise'],
        params['n_edges_noise'],
        params['seed_input_graph'],
        params['seed_embedding'],
        params['num_reads'],
        params['anneal_time'],
        params['pause_duration'],
        params['pause_start'],
        time_qubo,
        time_dwave_response,
        time_overall_computation,
        solution_frequency,
        runs_to_solution,
        input_graph,
        edges_solution,
        enriched_states_df.to_json(orient='records'),
        json.dumps(response.info['embedding_context'])
    ]]

    return data
