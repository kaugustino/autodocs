import glob
import click
from autodocs.autodoc import Autodoc


@click.command()
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    show_default=True,
    default=False,
    help="Prompt confirmation of each doctring change.",
)
@click.option(
    "-u",
    "--update",
    is_flag=True,
    show_default=True,
    default=False,
    help="Update existing docstrings.",
)
@click.argument(
    "target_paths",
    type=click.Path(exists=True, writable=True, resolve_path=True),
    nargs=-1,
    required=True,
)
def main(target_paths, interactive, update):
    autodoc = Autodoc(interactive, update)

    # TODO: if root_path is a file destination, second for loop is skipped
    for root_path in target_paths:
        for filename in glob.iglob(root_path + "/**/*.py", recursive=True):
            autodoc.add_source_tree(filename)
            autodoc.modify_source_tree(filename)
            autodoc.update_file_content(filename)
