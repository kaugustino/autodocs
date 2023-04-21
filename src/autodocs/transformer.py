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
            return updated_node.with_changes(
                body=cst.IndentedBlock(
                    body=[
                        cst.SimpleStatementLine(
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
                        ),
                        cst.SimpleStatementLine(
                            body=[
                                cst.Assign(
                                    targets=[
                                        cst.AssignTarget(
                                            target=cst.Name(
                                                value="lines",
                                                lpar=[],
                                                rpar=[],
                                            ),
                                            whitespace_before_equal=cst.SimpleWhitespace(
                                                value=" ",
                                            ),
                                            whitespace_after_equal=cst.SimpleWhitespace(
                                                value=" ",
                                            ),
                                        ),
                                    ],
                                    value=cst.Call(
                                        func=cst.Name(
                                            value="split_lines",
                                            lpar=[],
                                            rpar=[],
                                        ),
                                        args=[
                                            cst.Arg(
                                                value=cst.Name(
                                                    value="code",
                                                    lpar=[],
                                                    rpar=[],
                                                ),
                                                keyword=None,
                                                equal=cst.MaybeSentinel.DEFAULT,
                                                comma=cst.Comma(
                                                    whitespace_before=cst.SimpleWhitespace(
                                                        value="",
                                                    ),
                                                    whitespace_after=cst.SimpleWhitespace(
                                                        value=" ",
                                                    ),
                                                ),
                                                star="",
                                                whitespace_after_star=cst.SimpleWhitespace(
                                                    value="",
                                                ),
                                                whitespace_after_arg=cst.SimpleWhitespace(
                                                    value="",
                                                ),
                                            ),
                                            cst.Arg(
                                                value=cst.Name(
                                                    value="True",
                                                    lpar=[],
                                                    rpar=[],
                                                ),
                                                keyword=cst.Name(
                                                    value="keepends",
                                                    lpar=[],
                                                    rpar=[],
                                                ),
                                                equal=cst.AssignEqual(
                                                    whitespace_before=cst.SimpleWhitespace(
                                                        value="",
                                                    ),
                                                    whitespace_after=cst.SimpleWhitespace(
                                                        value="",
                                                    ),
                                                ),
                                                comma=cst.MaybeSentinel.DEFAULT,
                                                star="",
                                                whitespace_after_star=cst.SimpleWhitespace(
                                                    value="",
                                                ),
                                                whitespace_after_arg=cst.SimpleWhitespace(
                                                    value="",
                                                ),
                                            ),
                                        ],
                                        lpar=[],
                                        rpar=[],
                                        whitespace_after_func=cst.SimpleWhitespace(
                                            value="",
                                        ),
                                        whitespace_before_args=cst.SimpleWhitespace(
                                            value="",
                                        ),
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
                        ),
                        cst.SimpleStatementLine(
                            body=[
                                cst.Return(
                                    value=cst.Call(
                                        func=cst.Name(
                                            value="tokenize_lines",
                                            lpar=[],
                                            rpar=[],
                                        ),
                                        args=[
                                            cst.Arg(
                                                value=cst.Name(
                                                    value="lines",
                                                    lpar=[],
                                                    rpar=[],
                                                ),
                                                keyword=None,
                                                equal=cst.MaybeSentinel.DEFAULT,
                                                comma=cst.Comma(
                                                    whitespace_before=cst.SimpleWhitespace(
                                                        value="",
                                                    ),
                                                    whitespace_after=cst.SimpleWhitespace(
                                                        value=" ",
                                                    ),
                                                ),
                                                star="",
                                                whitespace_after_star=cst.SimpleWhitespace(
                                                    value="",
                                                ),
                                                whitespace_after_arg=cst.SimpleWhitespace(
                                                    value="",
                                                ),
                                            ),
                                            cst.Arg(
                                                value=cst.Name(
                                                    value="version_info",
                                                    lpar=[],
                                                    rpar=[],
                                                ),
                                                keyword=None,
                                                equal=cst.MaybeSentinel.DEFAULT,
                                                comma=cst.Comma(
                                                    whitespace_before=cst.SimpleWhitespace(
                                                        value="",
                                                    ),
                                                    whitespace_after=cst.SimpleWhitespace(
                                                        value=" ",
                                                    ),
                                                ),
                                                star="",
                                                whitespace_after_star=cst.SimpleWhitespace(
                                                    value="",
                                                ),
                                                whitespace_after_arg=cst.SimpleWhitespace(
                                                    value="",
                                                ),
                                            ),
                                            cst.Arg(
                                                value=cst.Name(
                                                    value="start_pos",
                                                    lpar=[],
                                                    rpar=[],
                                                ),
                                                keyword=cst.Name(
                                                    value="start_pos",
                                                    lpar=[],
                                                    rpar=[],
                                                ),
                                                equal=cst.AssignEqual(
                                                    whitespace_before=cst.SimpleWhitespace(
                                                        value="",
                                                    ),
                                                    whitespace_after=cst.SimpleWhitespace(
                                                        value="",
                                                    ),
                                                ),
                                                comma=cst.MaybeSentinel.DEFAULT,
                                                star="",
                                                whitespace_after_star=cst.SimpleWhitespace(
                                                    value="",
                                                ),
                                                whitespace_after_arg=cst.SimpleWhitespace(
                                                    value="",
                                                ),
                                            ),
                                        ],
                                        lpar=[],
                                        rpar=[],
                                        whitespace_after_func=cst.SimpleWhitespace(
                                            value="",
                                        ),
                                        whitespace_before_args=cst.SimpleWhitespace(
                                            value="",
                                        ),
                                    ),
                                    whitespace_after_return=cst.SimpleWhitespace(
                                        value=" ",
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
                        ),
                    ],
                    header=cst.TrailingWhitespace(
                        whitespace=cst.SimpleWhitespace(
                            value="",
                        ),
                        comment=None,
                        newline=cst.Newline(
                            value=None,
                        ),
                    ),
                    indent=None,
                    footer=[],
                )
            )
        return updated_node
