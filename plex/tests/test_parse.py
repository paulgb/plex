from unittest import TestCase

from ..cell_parser import parse_cell


class ParseTests(TestCase):
    def test_simple_assignment(self):
        r = parse_cell("a = 3")

        self.assertSetEqual({'a'}, r.outputs)

    def test_double_assignment(self):
        r = parse_cell("""
a = 3
b = 9
        """)

        self.assertSetEqual({'a', 'b'}, r.outputs)

    def test_tuple_assignment(self):
        r = parse_cell("""
a, b = 3, 4
        """)

        self.assertSetEqual({'a', 'b'}, r.outputs)

    def test_list_assignment(self):
        r = parse_cell("""
[a, b] = 3, 4
        """)

        self.assertSetEqual({'a', 'b'}, r.outputs)

    def test_nested_assignment(self):
        r = parse_cell("""
[(a,b),(c,d)] = (1,2),(3,4)
        """)

        self.assertSetEqual({'a', 'b', 'c', 'd'}, r.outputs)

    def test_func_def(self):
        r = parse_cell("""
def foo(a, b):
    c = d
        """)

        self.assertSetEqual({'foo'}, r.outputs)

    def test_simple_inputs(self):
        r = parse_cell('a = b')

        self.assertSetEqual({'b'}, r.inputs)

    def test_binop_input(self):
        r = parse_cell('a = b * c')

        self.assertSetEqual({'b', 'c'}, r.inputs)

    def test_funcall_input(self):
        r = parse_cell('a = b * f(c, d)')

        self.assertSetEqual({'b', 'c', 'd', 'f'}, r.inputs)

    def test_aug_assign(self):
        r = parse_cell('a += 1')

        self.assertSetEqual({'a'}, r.inputs)
        self.assertSetEqual({'a'}, r.outputs)

    def test_new_var(self):
        r = parse_cell("""
a = 4
b = a
        """)

        self.assertSetEqual(set(), r.inputs)
        self.assertSetEqual({'a', 'b'}, r.outputs)

    def test_var_in_func(self):
        r = parse_cell("""
def foo(a, b):
    return a + b + c
        """)

        self.assertSetEqual({'c'}, r.inputs)
        self.assertSetEqual({'foo'}, r.outputs)


class RunTests(TestCase):
    def test_run(self):
        r = parse_cell("""
a = b + 2
        """)

        self.assertDictEqual({'a': 4}, r.run({'b': 2}))

    def test_run_2(self):
        r = parse_cell("""
b += 1
a = b + 2
        """)

        self.assertDictEqual({'a': 5, 'b': 3}, r.run({'b': 2}))
