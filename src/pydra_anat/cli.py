from typing import Optional

import typer
from typing_extensions import Annotated

app = typer.Typer()


def version_callback(value: bool):
    from .__about__ import __version__

    if value:
        typer.echo(f"pydra-anat version {__version__}")
        raise typer.Exit()


@app.command()
def main(
    version: Annotated[Optional[bool], typer.Option("--version", callback=version_callback)] = None  # noqa
) -> None:
    ...
