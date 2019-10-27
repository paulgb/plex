# Adapted rom https://stackoverflow.com/a/26374977/992299

import ast
from typing import List


def node_to_string(node):
    if isinstance(node, ast.AST):
        fields = [(name, node_to_string(val)) for name, val in ast.iter_fields(
            node) if name not in ('left', 'right')]
        args = ', '.join(f'{name}={value}' for name, value in fields)
        rv = f'{node.__class__.__name__}({args})'
        return rv
    else:
        return repr(node)


def visit_ast(node, level: int, result: List[str]):
    result.append('  ' * level + node_to_string(node))
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    visit_ast(item, level+1, result)
        elif isinstance(value, ast.AST):
            visit_ast(value, level+1, result)


def ast_to_string(node):
    result = list()
    visit_ast(node, 0, result)
    return '\n'.join(result)
