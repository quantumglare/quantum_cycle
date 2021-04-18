import pandas as pd

from quantumglare.common import utils


def inspect_single_run(raw_df, tag):

    """

    :param :

    :return: None

    """
    df = raw_df[
        (raw_df['tag'] == tag)
    ].copy()

    print(len(df))

    print(df[['seed_input_graph', 'seed_embedding', 'solution_frequency']])

    print(df.columns)
    print(len(df))
    print(df.head())

    for j in range(len(df)):
        print(f'======{j}=========')
        solution_df = pd.read_json(df['dwave_solution_df'].values[j])
        print(solution_df)
        print(solution_df[['energy']].iloc[0].values)
        sol1 = utils.convert_list_of_strings_to_list_of_tuples(
            eval(solution_df[['state']].iloc[0].values[0])
        )
        # print(solution_df[['energy']].iloc[1].values)
        sol2 = utils.convert_list_of_strings_to_list_of_tuples(
            eval(solution_df[['state']].iloc[1].values[0])
        )

        print(sol1)
        print(sol2)
        print(set(sol1) - set(sol2))
        print(set(sol2) - set(sol1))


def main():
    raw_df = pd.read_csv("data/raw_data.csv")
    inspect_single_run(
        raw_df,
        'deafult_minorminer_n_cycles_45_cycle_length_4_n_edges_noise_96'
    )


if __name__ == '__main__':
    main()
