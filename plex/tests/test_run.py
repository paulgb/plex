from unittest import TestCase

from ..cell import Cell


class RunTests(TestCase):
    def test_run(self):
        r = Cell.from_string("""
a = b + 2
        """)

        self.assertDictEqual({'a': 4}, r.run({'b': 2}))

    def test_run_2(self):
        r = Cell.from_string("""
b += 1
a = b + 2
        """)

        self.assertDictEqual({'a': 5, 'b': 3}, r.run({'b': 2}))
