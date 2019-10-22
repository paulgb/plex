import ast

from .cell_parser import collect_body_vars


class Cell:
    def __init__(self, inputs, outputs, code):
        self.inputs = inputs
        self.outputs = outputs
        self.code = code

    def run(self, params):
        exec(self.code, globals(), params)
        return {p: params[p] for p in self.outputs}

    @staticmethod
    def from_string(cell: str):
        result = ast.parse(cell)
        names = collect_body_vars(result.body)
        code = compile(result, '<ast>', 'exec')
        return Cell(names.inputs, names.outputs, code)
