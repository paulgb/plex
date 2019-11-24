from unittest import TestCase

from ..cell import Cell
from ..name_mapper import map_names


class TestMapNames(TestCase):
    def assertMapping(self, statements, expected):
        cells = [Cell.from_string(s) for s in statements]
        mapping = map_names(cells, __builtins__)
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

    def test_global(self):
        cells = [
            'a = int("3")'
        ]

        expected = [
            ({}, {'a': ('a', 0)}),
        ]

        self.assertMapping(cells, expected)

    def test_funcdef_call(self):
        cells = [
            'def foo(a):\n  return a + 3',
            'foo(3)',
        ]

        expected = [
            ({}, {'foo': ('foo', 0)}),
            ({'foo': ('foo', 0)}, {}),
        ]

        self.assertMapping(cells, expected)

    def test_funcdef_call_ref(self):
        cells = [
            'b = 9',
            'def foo(a):\n  return a + b',
            'foo(3)',
        ]

        expected = [
            ({}, {'b': ('b', 0)}),
            ({'b': ('b', 0)}, {'foo': ('foo', 0)}),
            ({'foo': ('foo', 0)}, {}),
        ]

        self.assertMapping(cells, expected)
