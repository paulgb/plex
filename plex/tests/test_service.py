from unittest import TestCase

from ..service import Service


def update_cell_message(cell_index, new_value):
    return {
        'message': 'update_cell',
        'index': cell_index,
        'value': new_value,
    }


def running_cell_message(cell_index):
    return {
        'message': 'cell_status',
        'index': cell_index,
        'status': {
            'status': 'RUNNING',
            'value': None,
        },
    }


def cell_result_message(cell_index, result):
    return {
        'message': 'cell_status',
        'index': cell_index,
        'status': {
            'status': 'RAN',
            'value': result,
        },
    }


class TestService(TestCase):
    def setUp(self):
        self.service = Service()

    def assertMessage(self, message, expected):
        result = list(self.service.send_message(message))
        self.assertListEqual(result, expected)

    def testSimpleMessage(self):
        self.assertMessage(
            update_cell_message(0, 'a = 4'),
            [
                running_cell_message(0),
                cell_result_message(0, '4')
            ]
        )
