import libcst as cst
from typing import List, Tuple, Dict, Optional


class DocstringCollector(cst.CSTVisitor):
    """A read only parser that fetches any existing
    docstring for each Class and/or Function."""

    def __init__(self):
        # Stack to store the canonical name of the current class and/or function
        self.stack: List[Tuple[str, ...]] = []
        self.docstrings: Dict[
            Tuple[str, ...],  # key: tuple of canonical class/function name
            Optional[str],  # value: optional docstring
        ] = {}

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.stack.append(node.name.value)
        self.docstrings[tuple(self.stack)] = node.get_docstring()

    def leave_ClassDef(self, node: cst.ClassDef) -> None:
        self.stack.pop()

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.stack.append(node.name.value)
        self.docstrings[tuple(self.stack)] = node.get_docstring()
        return False

    def leave_FunctionDef(self, node: cst.FunctionDef) -> None:
        self.stack.pop()
