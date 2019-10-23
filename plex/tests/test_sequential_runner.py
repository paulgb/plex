from unittest import TestCase

from ..sequential_runner import SequentialRunner


class TestSequentialRunner(TestCase):
    def assertSequence(self, input_output_pairs):
        runner = SequentialRunner()

        for inp, exp in input_output_pairs:
            cell, value = inp
            result = runner.set_cell(cell, value)
            self.assertListEqual(exp, result)

    def test_basic_sequence(self):
        self.assertSequence([((0, 'a = 1'), [(0, '1')])])
