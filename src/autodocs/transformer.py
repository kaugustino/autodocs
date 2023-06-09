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
        key = tuple(self.stack)
        self.stack.pop()
        return self.update_node_body_with_docstring(key, updated_node)

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.stack.append(node.name.value)
        self.docstrings[tuple(self.stack)] = node.get_docstring()
        return False

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:
        key = tuple(self.stack)
        self.stack.pop()
        return self.update_node_body_with_docstring(key, updated_node)

    def update_node_body_with_docstring(
        self, key: tuple, updated_node: cst.CSTNode
    ) -> cst.CSTNode:
        if self.docstrings.get(key, 0) is not None:
            return updated_node

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
            if isinstance(updated_node.body.body, list):
                updated_node.body.body.insert(0, cst_docstring)
                return updated_node
            elif isinstance(updated_node.body.body, tuple):
                # ClassDef instance returns a body parameter of type tuple and
                # since tuples are immutable, this is a hackish workaround to
                # return an updated node
                updated_tuple_body = (cst_docstring,) + updated_node.body.body
                updated_indent_block = cst.IndentedBlock(
                    body=updated_tuple_body,
                    header=updated_node.body.header,
                    indent=updated_node.body.indent,
                    footer=updated_node.body.footer,
                )
                return updated_node.with_changes(body=updated_indent_block)

        return updated_node
