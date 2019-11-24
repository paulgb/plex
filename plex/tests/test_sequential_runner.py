from unittest import TestCase

from ..sequential_runner import SequentialRunner, CellStatus, CellValue


class TestSequentialRunner(TestCase):
    def assertGen(self, expected, generator):
        self.assertListEqual(expected, list(generator))

    def test_basic_sequence(self):
        runner = SequentialRunner()

        self.assertGen(
            [
                (0, CellValue(CellStatus.RUNNING)),
                (0, CellValue(CellStatus.RAN, '1'))
            ],
            runner.set_cell(0, 'a = 1')
        )

    def test_two_part_sequence(self):
        runner = SequentialRunner()

        self.assertGen(
            [
                (0, CellValue(CellStatus.RUNNING)),
                (0, CellValue(CellStatus.RAN, '1'))
            ],
            runner.set_cell(0, 'a = 1')
        )

        self.assertGen(
            [
                (1, CellValue(CellStatus.RUNNING)),
                (1, CellValue(CellStatus.RAN, '2'))
            ],
            runner.set_cell(1, 'b = a + 1')
        )

    def test_two_part_sequence_update(self):
        runner = SequentialRunner()

        self.assertGen(
            [
                (0, CellValue(CellStatus.RUNNING)),
                (0, CellValue(CellStatus.RAN, '1'))
            ],
            runner.set_cell(0, 'a = 1')
        )

        self.assertGen(
            [
                (1, CellValue(CellStatus.RUNNING)),
                (1, CellValue(CellStatus.RAN, '2'))
            ],
            runner.set_cell(1, 'b = a + 1')
        )

        self.assertGen(
            [
                (0, CellValue(CellStatus.RUNNING)),
                (1, CellValue(CellStatus.RUNNING)),
                (0, CellValue(CellStatus.RAN, '5')),
                (1, CellValue(CellStatus.RAN, '6')),
            ],
            runner.set_cell(0, 'a = 5')
        )

    def test_syntax_error(self):
        runner = SequentialRunner()

        self.assertGen(
            [
                (0, CellValue(CellStatus.ERROR, 'SyntaxError'))
            ],
            runner.set_cell(0, 'a =')
        )

    def test_runtime_error(self):
        runner = SequentialRunner()

        self.assertGen(
            [
                (1, CellValue(CellStatus.ERROR, 'NameError'))
            ],
            runner.set_cell(1, 'a')
        )

    def test_func_def(self):
        runner = SequentialRunner()

        self.assertGen(
            [
                (0, CellValue(CellStatus.RUNNING, None)),
                (0, CellValue(CellStatus.RAN, None))
            ],
            runner.set_cell(0, 'def foo(a):\n  return')
        )

    def test_global(self):
        runner = SequentialRunner()

        self.assertGen(
            [
                (0, CellValue(CellStatus.RUNNING, None)),
                (0, CellValue(CellStatus.RAN, '3'))
            ],
            runner.set_cell(0, 'int("3")')
        )

    """
    def test_func_def_and_call(self):
        runner = SequentialRunner()

        self.assertGen(
            [
                (0, CellValue(CellStatus.RUNNING, None)),
                (0, CellValue(CellStatus.RAN, '3'))
            ],
            runner.set_cell(0, 'a = 3')
        )

        self.assertGen(
            [
                (1, CellValue(CellStatus.RUNNING, None)),
                (1, CellValue(CellStatus.RAN, None))
            ],
            runner.set_cell(1, 'def foo(b):\n  return a + b')
        )

        self.assertGen(
            [
                (2, CellValue(CellStatus.RUNNING, None)),
                (2, CellValue(CellStatus.RAN, '8'))
            ],
            runner.set_cell(2, 'foo(5)')
        )
    """
