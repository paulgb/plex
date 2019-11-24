import ast
from unittest import TestCase

from ..cell_parser import collect_names_flat


class TestCollectNames(TestCase):
    def assertCollected(self, expression, expect_names,
                        expect_input_names=None):
        result, = ast.parse(expression).body
        name_set = collect_names_flat(result)

        print(name_set)
        self.assertSetEqual(expect_names, name_set.inputs)
        if expect_input_names is None:
            expect_input_names = set()

        self.assertSetEqual(expect_input_names, name_set.outputs)

    def test_collect_var_name(self):
        self.assertCollected('a', {'a'})

    def test_collect_assignment(self):
        self.assertCollected('a = b', {'b'}, {'a'})

    def test_collect_product(self):
        self.assertCollected('a = b * c', {'b', 'c'}, {'a'})

    def test_collect_index(self):
        self.assertCollected('a = b[c]', {'b', 'c'}, {'a'})

    def test_collect_assign_index(self):
        self.assertCollected('a[c] = b', {'a', 'b', 'c'}, {'a'})

    def test_collect_list(self):
        self.assertCollected('[a, [b, c]]', {'a', 'b', 'c'})

    def test_collect_dict(self):
        self.assertCollected('{a: b, c: "d"}', {'a', 'b', 'c'})

    def test_collect_attribute(self):
        self.assertCollected('a.b', {'a'})

    def test_collect_funccall(self):
        self.assertCollected('a.b()', {'a'})
