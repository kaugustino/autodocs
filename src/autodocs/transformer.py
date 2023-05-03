import libcst as cst
from typing import List, Tuple, Dict, Optional


class DocstringTransformer(cst.CSTTransformer):
    """A read write tree that adds docstring for each Class and/or Function."""

    def __init__(self, docstrings, interactive_flag: bool, update_flag: bool):
        # Stack to store the canonical name of the current class and/or function
        self.stack: List[Tuple[str, ...]] = []
        self.docstrings: Dict[
            Tuple[str, ...],  # key: tuple of canonical class/function name
            Optional[str],  # value: optional docstring
        ] = docstrings
        self.interactive_flag = interactive_flag
        self.update_flag = update_flag

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.stack.append(node.name.value)

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.CSTNode:
        key = tuple(self.stack)
        self.stack.pop()
        return self.create_node_with_docstring(key, updated_node)

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.stack.append(node.name.value)
        return False

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:
        key = tuple(self.stack)
        self.stack.pop()
        return self.create_node_with_docstring(key, updated_node)

    def create_node_with_docstring(
        self, key: tuple, updated_node: cst.CSTNode
    ) -> cst.CSTNode:
        is_empty_docstring = self.docstrings.get(key, 0) is None
        if not is_empty_docstring and not self.update_flag:
            return updated_node

        cst_docstring = self.generate_docstring_statement()

        if isinstance(updated_node, cst.FunctionDef):
            if not is_empty_docstring:
                updated_node = self.remove_docstring_function_def(updated_node)
            updated_node = self.insert_docstring_function_def(
                cst_docstring, updated_node
            )
        elif isinstance(updated_node, cst.ClassDef):
            if not is_empty_docstring:
                updated_node = self.remove_docstring_class_def(updated_node)
            updated_node = self.insert_docstring_class_def(cst_docstring, updated_node)
        return updated_node

    def remove_docstring_function_def(self, updated_node: cst.CSTNode) -> cst.CSTNode:
        updated_node.body.body.pop(0)
        return updated_node

    def remove_docstring_class_def(self, updated_node: cst.CSTNode) -> cst.CSTNode:
        updated_body_list = list(updated_node.body.body)
        updated_body_list.pop(0)
        updated_indent_block = cst.IndentedBlock(
            body=tuple(updated_body_list),
            header=updated_node.body.header,
            indent=updated_node.body.indent,
            footer=updated_node.body.footer,
        )
        return updated_node.with_changes(body=updated_indent_block)

    def insert_docstring_function_def(
        self, cst_docstring: cst.SimpleStatementLine, updated_node: cst.CSTNode
    ) -> cst.CSTNode:
        updated_node.body.body.insert(0, cst_docstring)
        return updated_node

    def insert_docstring_class_def(
        self, cst_docstring: cst.SimpleStatementLine, updated_node: cst.CSTNode
    ) -> cst.CSTNode:
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

    def generate_docstring_statement(self) -> cst.SimpleStatementLine:
        docstring = """EXAMPLE DOCSTRING."""  # insert openai api call

        return cst.SimpleStatementLine(
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
