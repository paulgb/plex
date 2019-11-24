from unittest import TestCase

from ..cell import Cell


class ParseTests(TestCase):
    def test_simple_assignment(self):
        r = Cell.from_string("a = 3")

        self.assertSetEqual({'a'}, r.outputs)

    def test_double_assignment(self):
        r = Cell.from_string("""
a = 3
b = 9
        """)

        self.assertSetEqual({'a', 'b'}, r.outputs)

    def test_tuple_assignment(self):
        r = Cell.from_string("""
a, b = 3, 4
        """)

        self.assertSetEqual({'a', 'b'}, r.outputs)

    def test_list_assignment(self):
        r = Cell.from_string("""
[a, b] = 3, 4
        """)

        self.assertSetEqual({'a', 'b'}, r.outputs)

    def test_nested_assignment(self):
        r = Cell.from_string("""
[(a,b),(c,d)] = (1,2),(3,4)
        """)

        self.assertSetEqual({'a', 'b', 'c', 'd'}, r.outputs)

    def test_func_def(self):
        r = Cell.from_string("""
def foo(a, b):
    c = d
        """)

        self.assertSetEqual({'foo'}, r.outputs)

    def test_simple_inputs(self):
        r = Cell.from_string('a = b')

        self.assertSetEqual({'b'}, r.inputs)

    def test_binop_input(self):
        r = Cell.from_string('a = b * c')

        self.assertSetEqual({'b', 'c'}, r.inputs)

    def test_funcall_input(self):
        r = Cell.from_string('a = b * f(c, d)')

        self.assertSetEqual({'b', 'c', 'd', 'f'}, r.inputs)

    def test_aug_assign(self):
        r = Cell.from_string('a += 1')

        self.assertSetEqual({'a'}, r.inputs)
        self.assertSetEqual({'a'}, r.outputs)

    def test_aug_assign2(self):
        r = Cell.from_string('a += b')

        self.assertSetEqual({'a', 'b'}, r.inputs)
        self.assertSetEqual({'a'}, r.outputs)

    def test_new_var(self):
        r = Cell.from_string("""
a = 4
b = a
        """)

        self.assertSetEqual(set(), r.inputs)
        self.assertSetEqual({'a', 'b'}, r.outputs)

    def test_var_in_func(self):
        r = Cell.from_string("""
def foo(a, b):
    return a + b + c
        """)

        self.assertSetEqual({'c'}, r.inputs)
        self.assertSetEqual({'foo'}, r.outputs)

    def test_index(self):
        r = Cell.from_string("""
a = b[c]
        """)

        self.assertSetEqual({'b', 'c'}, r.inputs)
        self.assertSetEqual({'a'}, r.outputs)

    def test_index_assignment(self):
        r = Cell.from_string("""
a[d] = b[c]
        """)

        self.assertSetEqual({'a', 'b', 'c', 'd'}, r.inputs)
        self.assertSetEqual({'a'}, r.outputs)

    def test_index_assignment2(self):
        r = Cell.from_string("""
a[b] = b[c]
        """)

        self.assertSetEqual({'a', 'b', 'c'}, r.inputs)
        self.assertSetEqual({'a'}, r.outputs)

    def test_index_assignment3(self):
        r = Cell.from_string(r"""
a = {}
a[b] = b[c]
        """)

        self.assertSetEqual({'b', 'c'}, r.inputs)
        self.assertSetEqual({'a'}, r.outputs)

    def test_multiple_assign(self):
        r = Cell.from_string("""
a = b = c
        """)

        self.assertSetEqual({'c'}, r.inputs)
        self.assertSetEqual({'a', 'b'}, r.outputs)

    def test_func_call(self):
        r = Cell.from_string("foo(a)")

        self.assertSetEqual({'a', 'foo'}, r.inputs)
        self.assertSetEqual(set(), r.outputs)
