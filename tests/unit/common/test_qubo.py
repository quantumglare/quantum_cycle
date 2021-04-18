import pytest
import numpy as np

from quantumglare.common import qubo


class TestGetQ:
    def test_one_cycle_no_penalties(self):
        edges = [(0, 1), (1, 2), (2, 0)]
        q = qubo.get_Q(edges)
        expected_q = {
            ('(0, 1)', '(0, 1)'): -1,
            ('(1, 2)', '(1, 2)'): -1,
            ('(2, 0)', '(2, 0)'): -1,
        }
        assert q == expected_q

    def test_max_one_out_penalty_one_edge_noise(self):
        edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
        q = qubo.get_Q(edges)
        expected_q = {
            ('(0, 1)', '(0, 1)'): -1,
            ('(1, 2)', '(1, 2)'): -1,
            ('(2, 0)', '(2, 0)'): -1,
            ('(2, 3)', '(2, 3)'): -1,

            # due to max one out constraint
            # note that the ('(2, 3)', '(2, 0)') is not explicitly set
            ('(2, 0)', '(2, 3)'): 1.01,
        }
        assert q == expected_q

    def test_max_one_in_penalty_two_edges_noise(self):
        edges = [(0, 1), (1, 2), (2, 0), (3, 1), (4, 1)]
        q = qubo.get_Q(edges)
        expected_q = {
            ('(0, 1)', '(0, 1)'): -1,
            ('(1, 2)', '(1, 2)'): -1,
            ('(2, 0)', '(2, 0)'): -1,
            ('(3, 1)', '(3, 1)'): -1,
            ('(4, 1)', '(4, 1)'): -1,

            # due to max one in constraint
            ('(3, 1)', '(0, 1)'): 1.01,
            ('(4, 1)', '(0, 1)'): 1.01,
            ('(3, 1)', '(4, 1)'): 1.01,
        }
        assert q == expected_q

    def test_no_pairs(self):
        edges = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 3)]
        q = qubo.get_Q(edges)
        expected_q = {
            ('(0, 1)', '(0, 1)'): -1,
            ('(1, 2)', '(1, 2)'): -1,
            ('(2, 0)', '(2, 0)'): -1,
            ('(3, 4)', '(3, 4)'): -1,
            ('(4, 3)', '(4, 3)'): -1,

            # due to no pairs constraint
            ('(3, 4)', '(4, 3)'): 2.01,
        }
        assert q == expected_q

    def test_all_constraints_violated(self):
        edges = [(0, 1), (1, 2), (2, 0), (2, 1)]
        q = qubo.get_Q(edges)
        expected_q = {
            ('(0, 1)', '(0, 1)'): -1,
            ('(1, 2)', '(1, 2)'): -1,
            ('(2, 0)', '(2, 0)'): -1,
            ('(2, 1)', '(2, 1)'): -1,
            # due to max one out constraint
            ('(2, 1)', '(2, 0)'): 1.01,
            # due to max one in constraint
            ('(2, 1)', '(0, 1)'): 1.01,
            # due to no pairs constraint
            ('(1, 2)', '(2, 1)'): 2.01,
        }
        assert q == expected_q


class TestCalculateEnergyForState:
    def test_individual_max_one_out_one_edge_noise(self):
        edges_problem = [(0, 1), (1, 2), (2, 0), (2, 3)]
        q = qubo.get_Q(edges_problem)

        state_triangle = [(0, 1), (1, 2), (2, 0)]
        energy_state_triangle = qubo.calculate_energy_for_state(q, state_triangle)

        state_max_one_out_violated = [(0, 1), (1, 2), (2, 0), (2, 3)]
        energy_state_max_one_out_violated = qubo.calculate_energy_for_state(q, state_max_one_out_violated)

        assert energy_state_max_one_out_violated > energy_state_triangle
        assert energy_state_triangle == -3
        assert np.isclose(energy_state_max_one_out_violated, -4 + 1.01)

    def test_individual_max_one_out_two_edges_noise(self):
        edges_problem = [(0, 1), (1, 2), (2, 0), (2, 3), (2, 4)]
        q = qubo.get_Q(edges_problem)

        state_triangle = [(0, 1), (1, 2), (2, 0)]
        energy_state_triangle = qubo.calculate_energy_for_state(q, state_triangle)

        state_max_one_out_violated_one_edge = [(0, 1), (1, 2), (2, 0), (2, 3)]
        energy_state_max_one_out_violated_one_edge = qubo.calculate_energy_for_state(q, state_max_one_out_violated_one_edge)

        state_max_one_out_violated_two_edges = [(0, 1), (1, 2), (2, 0), (2, 3), (2, 4)]
        energy_state_max_one_out_violated_two_edges = qubo.calculate_energy_for_state(q, state_max_one_out_violated_two_edges)

        assert energy_state_max_one_out_violated_one_edge > energy_state_triangle
        assert energy_state_max_one_out_violated_two_edges > energy_state_triangle
        assert energy_state_triangle == -3
        assert np.isclose(energy_state_max_one_out_violated_one_edge, -4 + 1.01)
        assert np.isclose(energy_state_max_one_out_violated_two_edges, -5 + 3 * 1.01)

    def test_individual_max_one_in_one_edge_noise(self):
        edges_problem = [(0, 1), (1, 2), (2, 0), (3, 2)]
        q = qubo.get_Q(edges_problem)

        state_triangle = [(0, 1), (1, 2), (2, 0)]
        energy_state_triangle = qubo.calculate_energy_for_state(q, state_triangle)

        state_max_one_in_violated = [(0, 1), (1, 2), (2, 0), (3, 2)]
        energy_state_max_one_in_violated = qubo.calculate_energy_for_state(q, state_max_one_in_violated)

        assert energy_state_max_one_in_violated > energy_state_triangle
        assert energy_state_triangle == -3
        assert np.isclose(energy_state_max_one_in_violated, -4 + 1.01)

    def test_individual_max_one_in_two_edges_noise(self):
        edges_problem = [(0, 1), (1, 2), (2, 0), (3, 2), (4, 2)]
        q = qubo.get_Q(edges_problem)

        state_triangle = [(0, 1), (1, 2), (2, 0)]
        energy_state_triangle = qubo.calculate_energy_for_state(q, state_triangle)

        state_max_one_in_violated_one_edge = [(0, 1), (1, 2), (2, 0), (3, 2)]
        energy_state_max_one_in_violated_one_edge = qubo.calculate_energy_for_state(q, state_max_one_in_violated_one_edge)

        state_max_one_in_violated_two_edges = [(0, 1), (1, 2), (2, 0), (3, 2), (4, 2)]
        energy_state_max_one_in_violated_two_edges = qubo.calculate_energy_for_state(q, state_max_one_in_violated_two_edges)

        assert energy_state_max_one_in_violated_one_edge > energy_state_triangle
        assert energy_state_max_one_in_violated_two_edges > energy_state_triangle
        assert energy_state_triangle == -3
        assert np.isclose(energy_state_max_one_in_violated_one_edge, -4 + 1.01)
        assert np.isclose(energy_state_max_one_in_violated_two_edges, -5 + 3 * 1.01)

    def test_individual_no_pairs(self):
        edges_problem = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 3)]
        q = qubo.get_Q(edges_problem)

        state_triangle = [(0, 1), (1, 2), (2, 0)]
        energy_state_triangle = qubo.calculate_energy_for_state(q, state_triangle)

        state_triangle_and_pair = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 3)]
        energy_state_triangle_and_pair = qubo.calculate_energy_for_state(q, state_triangle_and_pair)

        assert energy_state_triangle_and_pair > energy_state_triangle
        assert energy_state_triangle == -3
        assert np.isclose(energy_state_triangle_and_pair, -5 + 2.01)

    def test_constraint_max_one_in_and_max_one_out_one_edge_noise(self):
        edges_problem = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3)]
        q = qubo.get_Q(edges_problem)

        legit_state = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]
        energy_legit_state = qubo.calculate_energy_for_state(q, legit_state)

        forbidden_state = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3)]
        energy_forbidden_state = qubo.calculate_energy_for_state(q, forbidden_state)

        assert energy_forbidden_state > energy_legit_state
        assert energy_legit_state == -6
        assert energy_forbidden_state == -7 + 2 * 1.01

    def test_constraint_max_one_in_and_max_one_out_two_edges_noise(self):
        edges_problem = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3), (2, 5)]
        q = qubo.get_Q(edges_problem)

        legit_state = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]
        energy_legit_state = qubo.calculate_energy_for_state(q, legit_state)

        forbidden_state = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3), (2, 5)]
        energy_forbidden_state = qubo.calculate_energy_for_state(q, forbidden_state)

        assert energy_forbidden_state > energy_legit_state
        assert energy_legit_state == -6
        # the 1.01 * 3 is for the max one out violated once for 3 possible pairs
        # of edge and the 1.01 * 2 for the max one in violated twice
        assert np.isclose(energy_forbidden_state, -8 + 1.01 * 3 + 1.01 * 2)

    def test_constraint_no_pairs_square(self):
        edges_problem = [(0, 1), (1, 2), (2, 3), (3, 0), (2, 1), (0, 3)]
        q = qubo.get_Q(edges_problem)

        # the only legit solution here is the square as the pairs are forbidden
        legit_state = [(0, 1), (1, 2), (2, 3), (3, 0)]
        energy_legit_state = qubo.calculate_energy_for_state(q, legit_state)

        # the two pairs are a forbidden configuration
        forbidden_state = [(1, 2), (2, 1), (3, 0), (0, 3)]
        energy_forbidden_state = qubo.calculate_energy_for_state(q, forbidden_state)

        assert energy_forbidden_state > energy_legit_state
        assert energy_legit_state == -4
        assert energy_forbidden_state == -4 + 2 * 2.01

    def test_constraint_no_pairs_triangle(self):
        edges_problem = [(0, 1), (1, 2), (2, 0), (2, 1)]
        q = qubo.get_Q(edges_problem)

        legit_state = [(0, 1), (1, 2), (2, 0)]
        energy_legit_state = qubo.calculate_energy_for_state(q, legit_state)

        forbidden_state = [(0, 1), (1, 2), (2, 0), (2, 1)]
        energy_forbidden_state = qubo.calculate_energy_for_state(q, forbidden_state)

        assert energy_forbidden_state > energy_legit_state
        assert energy_legit_state == -3
        # there is a 1.01 for max one in, a 1.01 for max one in, a 1.01 for no pairs
        assert np.isclose(energy_forbidden_state, -4 + 1.01 + 1.01 + 2.01)



