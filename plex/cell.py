import ast

from .cell_parser import collect_body_vars


class Cell:
    def __init__(self, inputs, outputs, code):
        self.inputs = inputs
        self.outputs = outputs
        self.code = code

    def run(self, params):
        exec(self.code, globals(), params)
        return {p: params[p] for p in self.outputs | {'__out'}}

    @staticmethod
    def from_string(cell: str):
        result = ast.parse(cell)
        
        names = collect_body_vars(result.body)

        if isinstance(result.body[-1], ast.Expr):
            result.body[-1] = ast.Assign(
                [ast.Name('__out', lineno=0, col_offset=0, ctx=ast.Store())],
                result.body[-1].value, lineno=0, col_offset=0)
        elif isinstance(result.body[-1], ast.Assign):
            result.body[-1].targets.append(
                ast.Name('__out', lineno=0, col_offset=0, ctx=ast.Store()))
        
        code = compile(result, '<ast>', 'exec')
        return Cell(names.inputs, names.outputs, code)
