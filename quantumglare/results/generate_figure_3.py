from matplotlib import pyplot as plt
from matplotlib import rcParams
import pandas as pd


def plot_figure_3(processed_df: pd.DataFrame):

    """
    Create figure 43of the paper from input dataframe

    :param processed_df:

    :return: None

    """
    fig = plt.figure(figsize=(10, 5.5))
    ax = [fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)]

    default_lines_colours = [
        p['color'] for p in plt.rcParams['axes.prop_cycle']
    ]
    lines_colours = [
        'gray',
        default_lines_colours[0],
        default_lines_colours[1],
    ]
    markers = ['o', 'o', 'o']
    # Panel a - varying p_noise for cycle_length = 4
    labels = [
        "$0$",
        "$0.5$",
        "$1.0$",
    ]
    for j, p_noise in enumerate([0, 5e-5, 1e-4]):
        processed_df_tmp = processed_df[
            (processed_df['p_noise'] == p_noise) &
            (processed_df['cycle_length'] == 4)
        ].copy()

        ax[0].errorbar(
            processed_df_tmp['n_vertices'],
            processed_df_tmp['p_sol_avg'],
            yerr=processed_df_tmp['p_sol_err'],
            fmt=markers[j] + "--",
            label=labels[j],
            color=lines_colours[j],
            markersize=6,
        )

    ax[0].set_xlabel("$N_\\mathrm{V}$")
    ax[0].set_ylabel("$\\bar{P}_\\mathrm{sol}$")
    ax[0].set_ylim([0, 1.05])
    ax[0].legend(
        loc='lower left',
        title="$p_{\\mathrm{noise}}\\, (\\times 10^{-4})$"
    )
    markers = ['o', 'o', 'o']
    lines_colours = [
        default_lines_colours[2],
        default_lines_colours[0],
        default_lines_colours[4],
    ]
    # Panel b - varying cycle_length for p_noise = 5e-5
    for j, cycle_length in enumerate([3, 4, 5]):
        processed_df_tmp = processed_df[
            (processed_df['p_noise'] == 5e-5) &
            (processed_df['cycle_length'] == cycle_length)
        ].copy()
        ax[1].errorbar(
            processed_df_tmp['n_vertices'],
            processed_df_tmp['p_sol_avg'],
            yerr=processed_df_tmp['p_sol_err'],
            fmt=markers[j] + "--",
            label=f"{cycle_length}",
            color=lines_colours[j],
            markersize=6,
        )
    ax[1].set_xlabel("$N_\\mathrm{V}$")
    ax[1].set_ylabel("$\\bar{P}_\\mathrm{sol}$")
    ax[1].set_ylim([0, 1.05])
    ax[1].legend(title="$\\mathrm{{cycle\\;length}}$")

    ax[0].text(-0.15, 1.05, '(a)', fontsize=18, transform=ax[0].transAxes)
    ax[1].text(-0.15, 1.05, '(b)', fontsize=18, transform=ax[1].transAxes)

    plt.savefig(fname="data/figure_3.pdf")


def main():
    rcParams.update({'font.size': 14, 'figure.autolayout': True})

    processed_df = pd.read_csv("data/processed_data.csv")
    plot_figure_3(processed_df)


if __name__ == '__main__':
    main()
