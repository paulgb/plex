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
