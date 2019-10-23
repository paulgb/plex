from .cell import Cell
from typing import Dict

from .name_mapper import map_names


class SequentialRunner:
    def __init__(self):
        pass

    def set_cell(self, index: int, value: str):
        cell = Cell.from_string(value)

        result = cell.run({})

        if '__out' in result:
            return [(index, repr(result['__out']))]
        return []
