import libcst as cst
from typing import Dict
from autodocs.visitor import DocstringCollector
from autodocs.transformer import DocstringTransformer


class Autodoc:
    """Autodoc class interacts with the libcst library."""

    def __init__(self, interactive_flag: bool, update_flag: bool):
        self.interactive_flag: bool = interactive_flag
        self.update_flag: bool = update_flag
        self.source_trees: Dict[str, cst.Module] = {}
        self.modified_source_trees: Dict[str, cst.Module] = {}

    def add_source_tree(self, filename: str) -> None:
        with open(filename, "r") as file:
            file_content = file.read()

        self.source_trees[filename] = cst.parse_module(file_content)

    def modify_source_tree(self, filename: str) -> None:
        visitor = DocstringCollector()
        source_tree = self.source_trees[filename]
        source_tree.visit(visitor)

        transformer = DocstringTransformer(
            visitor.docstrings, self.interactive_flag, self.update_flag
        )

        # Must create new dict because original source tree does not update
        # changes to tuples since they are immutable
        self.modified_source_trees[filename] = source_tree.visit(transformer)

    def retrieve_modified_tree_code(self, filename: str) -> str:
        return self.modified_source_trees[filename].code
