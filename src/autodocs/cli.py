import click


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
def main(target_paths, interactive):
    click.echo(target_paths)
