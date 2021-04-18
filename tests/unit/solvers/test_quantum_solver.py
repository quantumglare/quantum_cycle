import pandas as pd
from quantumglare.solvers import quantum_solver


class TestGetValidSolutions:
    def test_one_solution(self):
        states_df = pd.DataFrame(
            columns=['state', 'energy', 'relative_frequency'],
            data=[
                ["['(1, 2)', '(2, 3)', '(3, 1)']", -3, 0.80],
                ["['(1, 2)', '(2, 3)']", -2, 0.15],
                ["['(1, 2)', '(3, 1)']", -2, 0.05],
        ]
        )
        input_graph = [(1, 2), (2, 3), (3, 1), (3, 2)]

        _, solution_frequency, solutions = quantum_solver.get_valid_solutions(
            states_df, input_graph
        )

        assert solution_frequency == 0.80
        assert solutions == [[(1, 2), (2, 3), (3, 1)]]

    def test_two_solutions(self):
        states_df = pd.DataFrame(
            columns=['state', 'energy', 'relative_frequency'],
            data=[
                ["['(1, 2)', '(2, 3)', '(3, 1)', '(4, 5)', '(5, 6)', '(6, 4)']", -6, 0.30],
                ["['(1, 2)', '(2, 3)', '(3, 4)', '(4, 5)', '(5, 6)', '(6, 1)']", -6, 0.50],
                ["['(1, 2)', '(2, 3)']", -2, 0.20],
        ]
        )
        input_graph = [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4), (3, 4), (6, 1)]

        _, solution_frequency, solutions = quantum_solver.get_valid_solutions(
            states_df, input_graph
        )

        assert solution_frequency == 0.80
        assert solutions == [
            [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)],
        ]
