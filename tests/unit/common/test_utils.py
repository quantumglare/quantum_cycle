import pytest

from quantumglare.common import graph, utils


class TestConvertListOfStringsToListOfLists:
    def test(self):
        output = utils.convert_list_of_strings_to_list_of_tuples(
            ['(12, 5)', '(5, 12)']
        )
        assert output == [(12, 5), (5, 12)]


class TestGetVertices:
    def test(self):
        edges = [(0, 1), (1, 2), (2, 0), (3, 4)]
        output = graph.get_vertices(edges)
        expected_output = [0, 1, 2, 3, 4]
        assert output == expected_output


class TestIsValid:
    def test_true(self):
        edges_input = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (0, 3)]
        edges_output = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]
        actual_is_legit_value = graph.is_valid(edges_output, edges_input)
        assert actual_is_legit_value is True

    def test_false_no_subset(self):
        edges_input = [(0, 1), (1, 2), (2, 0)]
        edges_output = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]
        actual_is_legit_value = graph.is_valid(edges_output, edges_input)
        assert actual_is_legit_value is False

    def test_false_not_all_vertices_covered(self):
        edges_input = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (0, 3)]
        edges_output = [(0, 1), (1, 2), (2, 0)]
        actual_is_legit_value = graph.is_valid(edges_output, edges_input)
        assert actual_is_legit_value is False

    def test_false_max_one_out_not_respected(self):
        edges_input = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (0, 3)]
        edges_output = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (0, 3)]
        actual_is_legit_value = graph.is_valid(edges_output, edges_input)
        assert actual_is_legit_value is False

    def test_false_max_one_in_not_respected(self):
        edges_input = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (3, 0)]
        edges_output = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (3, 0)]
        actual_is_legit_value = graph.is_valid(edges_output, edges_input)
        assert actual_is_legit_value is False

    def test_false_flow_not_conserved(self):
        edges_input = [(0, 1), (1, 2), (3, 4), (4, 5), (5, 3)]
        edges_output = [(0, 1), (1, 2), (3, 4), (4, 5), (5, 3)]
        actual_is_legit_value = graph.is_valid(edges_output, edges_input)
        assert actual_is_legit_value is False

    def test_false_cycles_of_length_two_present(self):
        edges_input = [(0, 1), (1, 0), (3, 4), (4, 5), (5, 3)]
        edges_output = [(0, 1), (1, 0), (3, 4), (4, 5), (5, 3)]
        actual_is_legit_value = graph.is_valid(edges_output, edges_input)
        assert actual_is_legit_value is False
