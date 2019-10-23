from .cell import Cell


class SequentialRunner:
    def __init__(self):
        pass

    def set_cell(self, index: int, value: str):
        cell = Cell.from_string(value)

        result = cell.run({})

        if '__out' in result:
            return [(index, repr(result['__out']))]
        return []
