import ast
from typing import Set
from functools import reduce
from operator import or_


def union(*collected_names):
    if not collected_names:
        return CollectedNames()
    return reduce(or_, collected_names)


class CollectedNames:
    def __init__(self, names=None, inputs=None, outputs=None):
        self.names = names or set()
        self.inputs = inputs or set()
        self.outputs = outputs or set()
        assert isinstance(self.names, set)
        assert isinstance(self.inputs, set)
        assert isinstance(self.outputs, set)

    def __repr__(self):
        return (f'CollectedNames(names={self.names}, '
                f'inputs={self.inputs}, '
                f'outputs={self.outputs})')

    def names_to_inputs(self):
        return CollectedNames(
            set(),
            self.inputs | self.names,
            self.outputs
        )

    def names_to_outputs(self):
        return CollectedNames(
            set(),
            self.inputs,
            self.outputs | self.names
        )

    def __or__(self, other: 'CollectedNames'):
        assert isinstance(other, CollectedNames)
        return CollectedNames(self.names | other.names,
                              self.inputs | other.inputs,
                              self.outputs | other.outputs)

    def __sub__(self, other: 'CollectedNames'):
        assert isinstance(other, CollectedNames)
        return CollectedNames(self.names - other.names,
                              self.inputs - other.inputs,
                              self.outputs - other.outputs)


def collect_names(elem) -> CollectedNames:
    if isinstance(elem, list):
        return union(*(collect_names(e) for e in elem))
    if isinstance(elem, (ast.Tuple, ast.List)):
        return union(*(collect_names(e) for e in elem.elts))
    elif isinstance(elem, ast.Num):
        return CollectedNames()
    elif isinstance(elem, ast.Name):
        return CollectedNames({elem.id})
    elif isinstance(elem, ast.BinOp):
        return collect_names(elem.left) | collect_names(elem.right)
    elif isinstance(elem, ast.Expr):
        return collect_names(elem.value)
    elif isinstance(elem, ast.FunctionDef):
        names = collect_body_vars(elem.body)
        args = {a.arg for a in elem.args.args}
        return CollectedNames(names.inputs - args) | CollectedNames(
            outputs={elem.name})
    elif isinstance(elem, ast.Return):
        return collect_names(elem.value)
    elif isinstance(elem, ast.Call):
        return (union(*(collect_names(c) for c in elem.args)) |
                CollectedNames({elem.func.id}))
    elif isinstance(elem, ast.Subscript):
        return (collect_names(elem.value) |
                collect_names(elem.value).names_to_inputs() |
                collect_names(elem.slice.value).names_to_inputs())
    elif isinstance(elem, ast.Assign):
        return (collect_names(elem.value) |
                union(*(collect_names(t).names_to_outputs()
                        for t in elem.targets)))
    elif isinstance(elem, ast.AugAssign):
        rec = collect_names(elem.target)
        return (rec
                | rec.names_to_outputs()
                | collect_names(elem.value))
    elif isinstance(elem, ast.Dict):
        return (union(*(collect_names(e) for e in elem.keys))
                | union(*(collect_names(e) for e in elem.values)))
    elif isinstance(elem, ast.If):
        return collect_names(elem.test) | collect_names(elem.body)
    elif isinstance(elem, (ast.Str, ast.NameConstant, ast.Pass)):
        return CollectedNames()
    else:
        assert False, elem
        return CollectedNames()


def collect_names_flat(elem):
    return collect_names(elem).names_to_inputs()


def collect_body_vars(body):
    outputs: Set[str] = set()
    inputs: Set[str] = set()

    for statement in body:
        names = collect_names_flat(statement)
        inputs.update(names.inputs - outputs)
        outputs.update(names.outputs)

    return CollectedNames(inputs=inputs, outputs=outputs)
