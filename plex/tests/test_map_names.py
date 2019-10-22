from unittest import TestCase

from ..cell import Cell
from ..name_mapper import map_names


class TestMapNames(TestCase):
    def assertMapping(self, statements, expected):
        cells = [Cell.from_string(s) for s in statements]
        mapping = map_names(cells)
        self.assertListEqual(expected, mapping)

    def test_simple_map(self):
        cells = [
            'a = 4'
        ]

        expected = [
            ({}, {'a': ('a', 0)})
        ]

        self.assertMapping(cells, expected)

    def test_simple_map2(self):
        cells = [
            'a = 4',
            'a += 1'
        ]

        expected = [
            ({}, {'a': ('a', 0)}),
            ({'a': ('a', 0)}, {'a': ('a', 1)})
        ]

        self.assertMapping(cells, expected)

    def test_simple_map3(self):
        cells = [
            'a = 4',
            'b = a + 1',
            'a += b',
        ]

        expected = [
            ({}, {'a': ('a', 0)}),
            ({'a': ('a', 0)}, {'b': ('b', 0)}),
            ({'a': ('a', 0), 'b': ('b', 0)}, {'a': ('a', 1)})
        ]

        self.assertMapping(cells, expected)
