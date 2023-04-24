import libcst as cst
from typing import List, Tuple, Dict, Optional


class DocstringTransformer(cst.CSTTransformer):
    """A read write tree that adds docstring for each Class and/or Function."""

    def __init__(self, docstrings):
        # Stack to store the canonical name of the current class and/or function
        self.stack: List[Tuple[str, ...]] = []
        self.docstrings: Dict[
            Tuple[str, ...],  # key: tuple of canonical class/function name
            Optional[str],  # value: optional docstring
        ] = docstrings

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.stack.append(node.name.value)

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.CSTNode:
        self.stack.pop()
        return updated_node

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.stack.append(node.name.value)
        self.docstrings[tuple(self.stack)] = node.get_docstring()
        return False

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:
        key = tuple(self.stack)
        self.stack.pop()
        if key in self.docstrings:
            docstring = self.docstrings[key]
            if not docstring:
                docstring = """EXAMPLE DOCSTRING."""  # insert openai api call
                cst_docstring = cst.SimpleStatementLine(
                    body=[
                        cst.Expr(
                            value=cst.SimpleString(
                                value=f'"""{docstring}"""',
                                lpar=[],
                                rpar=[],
                            ),
                            semicolon=cst.MaybeSentinel.DEFAULT,
                        ),
                    ],
                    leading_lines=[],
                    trailing_whitespace=cst.TrailingWhitespace(
                        whitespace=cst.SimpleWhitespace(
                            value="",
                        ),
                        comment=None,
                        newline=cst.Newline(
                            value=None,
                        ),
                    ),
                )
                if isinstance(updated_node.body, cst.IndentedBlock):
                    updated_node.body.body.insert(0, cst_docstring)
        return updated_node
