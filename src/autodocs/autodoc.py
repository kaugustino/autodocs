import libcst as cst
from typing import Dict
from autodocs.visitor import DocstringCollector
from autodocs.transformer import DocstringTransformer


class Autodoc:
    def __init__(self, interactive: bool, update: bool):
        self.interactive_flag: bool = interactive
        self.update_flag: bool = update
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

        transformer = DocstringTransformer(visitor.docstrings)
        self.modified_source_trees[filename] = source_tree.visit(transformer)

    def update_file_content(self, filename: str) -> None:
        new_file_content = self.modified_source_trees[filename].code
        with open(filename, "w") as file:
            file.write(new_file_content)
