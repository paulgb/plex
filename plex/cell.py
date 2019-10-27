import ast

from .cell_parser import collect_body_vars


class Cell:
    def __init__(self, inputs, outputs, code, collect_output):
        self.inputs = inputs
        self.outputs = outputs
        self.code = code
        self.collect_output = collect_output

    def run(self, params):
        exec(self.code, globals(), params)
        if self.collect_output:
            return {p: params[p] for p in self.outputs | {'__out'}}
        else:
            return {p: params[p] for p in self.outputs}

    @staticmethod
    def from_string(cell: str):
        result = ast.parse(cell)

        names = collect_body_vars(result.body)
        collect_output = True

        if isinstance(result.body[-1], ast.Expr):
            result.body[-1] = ast.Assign(
                [ast.Name('__out', lineno=0, col_offset=0, ctx=ast.Store())],
                result.body[-1].value, lineno=0, col_offset=0)
        elif isinstance(result.body[-1], ast.Assign):
            result.body[-1].targets.append(
                ast.Name('__out', lineno=0, col_offset=0, ctx=ast.Store()))
        elif isinstance(result.body[-1], ast.AugAssign):
            result.body.append(
                ast.Assign([
                    ast.Name('__out', lineno=0, col_offset=0, ctx=ast.Store())
                ], ast.Name(result.body[-1].target.id, lineno=0,
                            col_offset=0,
                            ctx=ast.Load()), lineno=0,
                            col_offset=0,
                            ctx=ast.Load()
                ))
        else:
            collect_output = False

        code = compile(result, '<ast>', 'exec')
        return Cell(names.inputs, names.outputs, code, collect_output)
