import os
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
@click.option(
    "-d",
    "--dry-run",
    "dry_run",
    is_flag=True,
    show_default=True,
    default=False,
    help="Dry run to print changes to stdout without writing to target files.",
)
@click.argument(
    "target_paths",
    type=click.Path(exists=True, writable=True, resolve_path=True),
    nargs=-1,
    required=True,
)
def main(target_paths, interactive: bool, update: bool, dry_run: bool):
    autodoc = Autodoc(interactive, update)

    for root_path in target_paths:
        if os.path.isdir(root_path):
            for filename in glob.iglob(root_path + "/**/*.py", recursive=True):
                run_autodoc(autodoc, filename, dry_run)
        elif os.path.isfile(root_path):
            run_autodoc(autodoc, root_path, dry_run)


def run_autodoc(autodoc: Autodoc, filename: str, dry_run: bool) -> None:
    autodoc.add_source_tree(filename)
    autodoc.modify_source_tree(filename)
    new_file_content = autodoc.retrieve_modified_tree_code(filename)

    if dry_run:
        # TODO: Update to use diffs instead
        print(f"File name: {filename}")
        print("New file content:")
        print(new_file_content)
        return

    with open(filename, "w") as file:
        file.write(new_file_content)
