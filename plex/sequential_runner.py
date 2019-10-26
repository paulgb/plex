from .cell import Cell
from .name_mapper import map_names
from enum import Enum


class CellStatus(Enum):
    RUNNING = 0
    RAN = 1
    ERROR = 2


class CellValue:
    def __init__(self, status=CellStatus, value=None):
        self.status = status
        self.value = value

    def __eq__(self, other):
        return (self.status, self.value) == (other.status, other.value)

    def __repr__(self):
        return f'CellValue({self.status}, {self.value})'


class SequentialRunner:
    def __init__(self):
        self.cells = dict()
        self.values = dict()

    def set_cell(self, index: int, value: str):
        cell = Cell.from_string(value)
        self.cells[index] = cell

        cell_indices = list(sorted(self.cells))

        mapped_cells = dict(zip(cell_indices, map_names(
            self.cells[i] for i in cell_indices)))

        _, changed_outputs = mapped_cells[index]
        changed_outputs = set(changed_outputs)
        cells_to_run = list()

        for i in cell_indices:
            inps, outs = mapped_cells[i]

            if set(inps) & set(changed_outputs) or i == index:
                changed_outputs |= set(outs)
                cells_to_run.append(i)
                yield (i, CellValue(CellStatus.RUNNING))

        for i in cells_to_run:
            cell = self.cells[i]
            inps, outs = mapped_cells[i]

            input_vars = {
                name: self.values[mapped_name]
                for name, mapped_name
                in inps.items()
            }

            result = cell.run(input_vars)

            self.values.update({
                mapped_name: result[name]
                for name, mapped_name
                in outs.items()
            })

            if '__out' in result:
                yield (i, CellValue(CellStatus.RAN, repr(result['__out'])))
            else:
                yield (i, None)
