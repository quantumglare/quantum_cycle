from matplotlib import pyplot as plt
from matplotlib import rcParams
import pandas as pd
import numpy as np
from scipy import optimize as opt


def plot_figure_4(processed_df: pd.DataFrame):

    """
    Create figure 4 of the paper from input dataframes

    :param processed_df:

    :return: None

    """
    fig = plt.figure(figsize=(10, 5.5))
    ax = [fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)]

    default_lines_colours = [
        p['color'] for p in plt.rcParams['axes.prop_cycle']
    ]
    lines_colours = [
        default_lines_colours[3],
        default_lines_colours[2],
    ]
    markers = ['o', '^']

    start_fit = 400

    n_vertices_list = [1000, 4000]
    a_exp = []
    a_exp_err = []
    a_power = []
    a_power_err = []
    b_exp = []
    b_exp_err = []
    b_power = []
    b_power_err = []
    for j, n_vertices in enumerate(n_vertices_list):
        print(n_vertices)
        processed_df_tmp = processed_df[
            (processed_df['n_vertices'] == n_vertices) &
            (processed_df['cycle_length'] == 4)
        ].sort_values(by='n_edges_noise').copy()

        # Panel a
        ax[0].errorbar(
            processed_df_tmp['n_edges_noise'],
            processed_df_tmp['p_sol_avg'],
            yerr=processed_df_tmp['p_sol_err'],
            fmt=markers[j]+"--",
            label=f"${n_vertices}$",
            color=lines_colours[j],
            markersize=6,
        )

        # Panel b - corresponding TTS
        x = processed_df_tmp[
            processed_df_tmp['n_edges_noise'] >= start_fit
        ]['n_edges_noise']
        y = np.log(processed_df_tmp[
            processed_df_tmp['n_edges_noise'] >= start_fit
        ]['tts_avg'])
        ax[1].errorbar(
            x=processed_df_tmp['n_edges_noise'],
            y=processed_df_tmp['tts_avg'],
            yerr=processed_df_tmp['tts_err'],
            fmt=markers[j],
            label=f"${n_vertices}$",
            color=lines_colours[j],
            markersize=6,
        )

        x_fit = np.linspace(start_fit, 1200, 1000)
        # exponential fit
        pars, cov = opt.curve_fit(
            lambda t, a, b: a + b * t,
            x,
            y,
            p0=(1e-3, 1e-3)
        )
        a, b = pars
        a_exp.append(a)
        a_exp_err.append(np.sqrt(cov[0][0]))
        b_exp.append(b)
        b_exp_err.append(np.sqrt(cov[1][1]))
        y_fit = np.exp(a + b * x_fit)
        ax[1].plot(x_fit, y_fit, ":", color=lines_colours[j])

        # power law fit
        pars, cov = opt.curve_fit(
            lambda t, a, b: a + b * np.log(t),
            x,
            y,
            p0=(1e-2, 1),
            maxfev=10000,
        )
        a, b = pars
        a_power.append(a)
        a_power_err.append(np.sqrt(cov[0][0]))
        b_power.append(b)
        b_power_err.append(np.sqrt(cov[1][1]))
        y_fit = np.exp(a + b * np.log(x_fit))
        ax[1].plot(x_fit, y_fit, color=lines_colours[j])

    ax[0].set_xlabel("$N_\\mathrm{noise}$")
    ax[0].set_ylabel("$\\bar{P}_\\mathrm{sol}$")
    ax[0].set_xlim([-50, 1250])
    ax[0].set_ylim([0, 1.05])
    ax[0].legend(title="$N_\\mathrm{V}$")

    ax[1].set_xlabel("$N_\\mathrm{noise}$")
    ax[1].set_ylabel("$\\mathrm{TTS\\;[ms]}$", labelpad=-10)
    ax[1].set_xlim([-50, 1250])
    ax[1].set_ylim([0.2, 50])
    ax[1].set_yscale('log')
    ax[1].legend(title="$N_\\mathrm{V}$")

    ax[0].text(
        -0.15, 1.05, '(a)', fontsize=18, transform=ax[0].transAxes
    )
    ax[1].text(
        -0.15, 1.05, '(b)', fontsize=18, transform=ax[1].transAxes
    )

    plt.savefig(fname="data/figure_4.pdf")

    print('== exponential fit parameters ==')
    print(f'a: {a_exp}')
    print(f'a_err: {a_exp_err}')
    print(f'b: {b_exp}')
    print(f'b_err: {b_exp_err}')

    print('== power law fit parameters ==')
    print(f'a: {a_power}')
    print(f'a_err: {a_power_err}')
    print(f'b: {b_power}')
    print(f'b_err: {b_power_err}')

    print(np.log(2))


def main():
    rcParams.update({'font.size': 14, 'figure.autolayout': True})

    processed_df = pd.read_csv("data/processed_data.csv")
    plot_figure_4(processed_df)


if __name__ == '__main__':
    main()
