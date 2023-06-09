from pathlib import Path
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
    input_image: Annotated[Path, typer.Argument(file_okay=True, resolve_path=True)],
    output_dir: Annotated[Path, typer.Argument(dir_okay=True, resolve_path=True)],
    input_mask: Annotated[
        Optional[Path], typer.Option("--input-mask", file_okay=True, resolve_path=True)
    ] = None,
    template_image: Annotated[
        Optional[Path], typer.Option("--template-image", file_okay=True, resolve_path=True)
    ] = None,
    template_mask: Annotated[
        Optional[Path], typer.Option("--template-mask", file_okay=True, resolve_path=True)
    ] = None,
    cache_dir: Annotated[
        Optional[Path], typer.Option("--cache-dir", dir_okay=True, resolve_path=True)
    ] = None,
    version: Annotated[Optional[bool], typer.Option("--version", callback=version_callback)] = None  # noqa
) -> None:
    from .workflows import pydra_anat, run

    workflow = pydra_anat(name="pydra_anat", cache_dir=cache_dir)
    workflow.inputs.input_image = input_image
    workflow.inputs.input_mask = input_mask
    workflow.inputs.template_image = template_image
    workflow.inputs.template_mask = template_mask

    result = run(workflow)
    typer.echo(result)
