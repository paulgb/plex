from .cell import Cell
from .name_mapper import map_names
from enum import Enum
from typing import Generator, Tuple


class CellStatus(Enum):
    RUNNING = 0
    RAN = 1
    ERROR = 2


class CellValue:
    def __init__(self, status=CellStatus, value=None):
        self.status = status
        self.value = str(value) if value is not None else None

    def __eq__(self, other):
        return (self.status, self.value) == (other.status, other.value)

    def __repr__(self):
        return f'CellValue({self.status}, {repr(self.value)})'

    def to_dict(self):
        return {
            'status': self.status.name,
            'value': self.value
        }


class SequentialRunner:
    def __init__(self):
        self.cells = dict()
        self.values = dict()

    def set_cell(self, index: int, value: str) -> Generator[
            Tuple[int, CellValue], None, None]:
        try:
            cell = Cell.from_string(value)
        except SyntaxError:
            yield (index, CellValue(CellStatus.ERROR, 'SyntaxError'))
            return
        self.cells[index] = cell

        cell_indices = list(sorted(self.cells))

        try:
            mapped_cells = dict(zip(cell_indices, map_names(
                (self.cells[i] for i in cell_indices), __builtins__)))
        except NameError as e:
            i, v = e.args
            ix = cell_indices[i]
            yield (ix, CellValue(CellStatus.ERROR, 'NameError'))
            return

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

            try:
                result = cell.run(input_vars)
            except Exception as e:
                yield (i, CellValue(CellStatus.ERROR, str(e)))
                break

            self.values.update({
                mapped_name: result[name]
                for name, mapped_name
                in outs.items()
            })

            yield (i, CellValue(CellStatus.RAN, result.get('__out', None)))
