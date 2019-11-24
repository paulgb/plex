from .cell import Cell
from typing import Iterable, Generator, List, Tuple, Dict

Mapping = Dict[str, Tuple[str, int]]
InOutMappings = Tuple[Mapping, Mapping]


def gen_map_names(cells: Iterable[Cell], globs: set) -> Generator[
        InOutMappings, None, None]:
    mapping = dict()
    for i, cell in enumerate(cells):
        inputs = dict()
        outputs = dict()
        for inp in cell.inputs:
            if inp not in mapping:
                if inp in globs:
                    continue
                raise NameError(i, inp)
            inputs[inp] = mapping[inp]
        for out in cell.outputs:
            if out in mapping:
                _, i = mapping[out]
                mapping[out] = (out, i+1)
            else:
                mapping[out] = (out, 0)
            outputs[out] = mapping[out]
        yield inputs, outputs


def map_names(cells: Iterable[Cell], globs: set = set()
              ) -> List[InOutMappings]:
    return list(gen_map_names(cells, globs))
