from .cell import Cell
from typing import Iterable, Generator, List, Tuple, Dict

Mapping = Dict[str, Tuple[str, int]]
InOutMappings = Tuple[Mapping, Mapping]


def gen_map_names(cells: Iterable[Cell]) -> Generator[
        InOutMappings, None, None]:
    mapping = dict()
    for cell in cells:
        inputs = dict()
        outputs = dict()
        for inp in cell.inputs:
            assert inp in mapping
            inputs[inp] = mapping[inp]
        for out in cell.outputs:
            if out in mapping:
                _, i = mapping[out]
                mapping[out] = (out, i+1)
            else:
                mapping[out] = (out, 0)
            outputs[out] = mapping[out]
        yield inputs, outputs


def map_names(cells: Iterable[Cell]) -> List[InOutMappings]:
    return list(gen_map_names(cells))
