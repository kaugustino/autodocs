import libcst as cst
from visitor import DocstringCollector
from transformer import DocstringTransformer


py_source = '''
class PythonToken(Token):
    def __repr__(self):
        return ('TokenInfo(type=%s, string=%r, start_pos=%r, prefix=%r)' %
                self._replace(type=self.type.name))

def tokenize(code, version_info, start_pos=(1, 0)):
    """Generate tokens from a the source code (string)."""
    lines = split_lines(code, keepends=True)
    return tokenize_lines(lines, version_info, start_pos=start_pos)
'''

visitor = DocstringCollector()
source_tree = cst.parse_module(py_source)

source_tree.visit(visitor)

transformer = DocstringTransformer(visitor.docstrings)
modified_tree = source_tree.visit(transformer)

print(modified_tree.code)
