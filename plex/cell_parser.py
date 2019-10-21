import ast
from typing import Set


class Cell:
    def __init__(self, inputs, outputs, code):
        self.inputs = inputs
        self.outputs = outputs
        self.code = code

    def run(self, params):
        exec(self.code, globals(), params)
        return {p: params[p] for p in self.outputs}


def collect_names(elem):
    if isinstance(elem, (ast.Tuple, ast.List)):
        return set.union(*(collect_names(e) for e in elem.elts))
    elif isinstance(elem, ast.Name):
        return {elem.id}
    elif isinstance(elem, ast.BinOp):
        return collect_names(elem.left) | collect_names(elem.right)
    elif isinstance(elem, ast.Expr):
        return collect_names(elem.value)
    elif isinstance(elem, ast.Call):
        return set.union({elem.func.id}, *(collect_names(c)
                                           for c in elem.args))
    else:
        return set()


def collect_statement_vars(statement):
    if isinstance(statement, ast.Assign):
        return (collect_names(statement.value),
                collect_names(statement.targets[0]))
    if isinstance(statement, ast.AugAssign):
        rec = collect_names(statement.target)
        return rec, rec | collect_names(statement.value)
    elif isinstance(statement, ast.FunctionDef):
        inputs, outputs = collect_body_vars(statement.body)
        args = {a.arg for a in statement.args.args}
        return inputs - args, {statement.name}
    elif isinstance(statement, ast.Return):
        return collect_names(statement.value), set()
    else:
        return set(), set()


def collect_body_vars(body):
    outputs: Set[str] = set()
    inputs: Set[str] = set()

    for statement in body:
        i_, o_ = collect_statement_vars(statement)
        inputs.update(i_ - outputs)
        outputs.update(o_)

    return inputs, outputs


def parse_cell(cell: str):
    result = ast.parse(cell)

    inputs, outputs = collect_body_vars(result.body)

    code = compile(result, '<ast>', 'exec')

    return Cell(inputs, outputs, code)
