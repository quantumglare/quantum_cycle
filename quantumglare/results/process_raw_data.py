import pandas as pd
import numpy as np
import os


def process_raw_data(df: pd.DataFrame, csv_name: str):
    """
    :param df:
    :param csv_name:

    :return: None

    """
    tags = df.tag.unique()

    processed_df = pd.DataFrame()

    # check no duplicates are present in raw data
    cols = [
        'n_vertices',
        'cycle_length',
        'n_edges_noise',
        'seed_input_graph',
        'seed_embedding',
    ]
    assert len(df[cols]) == len(df[cols].drop_duplicates()), \
        'duplicates present'

    for tag in tags:
        tmp_df = df[df.tag == tag].copy()
        # check that we have 50 seeds for each tag
        # assert len(tmp_df['seed'].unique()) == 50,\
        #     f'{tag} does not have 50 seeds'
        t_quantum_schedule = tmp_df.anneal_time.values[0] \
            + tmp_df.pause_duration.values[0]

        freqs = tmp_df.solution_frequency.sort_values()
        n_observations = len(freqs)
        p_sol_avg = freqs.mean()
        p_sol_err = freqs.std() / np.sqrt(n_observations)

        tts_avg = 1e-3 * t_quantum_schedule * np.log(1 - 0.99) \
            / np.log(1 - p_sol_avg)
        tts_err = 1e-3 * t_quantum_schedule * p_sol_err * np.abs(
            np.log(1 - 0.99) / ((1 - p_sol_avg) * np.log(1 - p_sol_avg) ** 2)
        )

        row_df = pd.DataFrame(
            {"tag": tag,
             "n_observations": n_observations,
             "n_cycles":  tmp_df.n_cycles.values[0],
             "cycle_length": tmp_df.cycle_length.values[0],
             "n_vertices": tmp_df.n_vertices.values[0],
             "p_noise": tmp_df.p_noise.values[0],
             "n_edges_noise": tmp_df.n_edges_noise.values[0],
             "p_sol_avg": p_sol_avg,
             "p_sol_err": p_sol_err,
             "tts_avg": tts_avg,
             "tts_err": tts_err,
             },
            index=[0],
        )

        processed_df = processed_df.append(row_df)

    processed_df.to_csv(os.path.join('data', f'{csv_name}'), index=False)


def main():
    print('start reading raw data')
    raw_df = pd.read_csv(os.path.join('data', 'raw_data.csv'))
    print('end reading raw data')
    process_raw_data(raw_df, 'processed_data.csv')


if __name__ == '__main__':
    main()
