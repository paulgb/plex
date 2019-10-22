from unittest import TestCase

from ..cell import Cell
from ..name_mapper import map_names


class TestMapNames(TestCase):
    def assertMapping(self, statements, expected):
        cells = [Cell.from_string(s) for s in statements]
        mapping = map_names(cells)
        self.assertListEqual(expected, mapping)

    def test_simple_dag(self):
        cells = [
            'a = 4'
        ]

        expected = [
            ({}, {'a': ('a', 0)})
        ]

        self.assertMapping(cells, expected)
