import base64
import zlib
from pathlib import Path

import typer
import requests

from jinja2 import Environment, FileSystemLoader


app = typer.Typer(
    help="Visualize the topology",
)


class TopologyError(Exception):
    ...


def _get_topology():
    try:
        #  TODO: Implement the logic to collect the topology using NAPALM
        #  Feel free to use Nornir
        raise NotImplementedError()
    except NotImplementedError as exc:
        raise TopologyError("TODO not implemented yet") from exc


def _kroki_get_url(base_url: str, diagram: str):
    encoded_diagram = base64.urlsafe_b64encode(zlib.compress(diagram.encode(), 9))
    return f"{base_url}{encoded_diagram.decode()}"


@app.callback()
def template_environment(
    ctx: typer.Context, template_location: Path = Path("topology_visualizer/templates")
) -> None:
    env = Environment(
        loader=FileSystemLoader(template_location),
        lstrip_blocks=False,
        trim_blocks=True,
    )
    ctx.obj = env


@app.command()
def graphviz(ctx: typer.Context, output: Path = "graphviz.svg") -> None:
    """
    Visualize the topology with graphviz
    """
    try:
        _get_topology()

    except TopologyError as exc:
        typer.echo(f"Error: {exc}", err=True)
        typer.echo("Collecting the topology failed", err=True)
        raise typer.Exit(1)

    env: Environment = ctx.obj
    template = env.get_template("graphiz.j2")

    #  TODO Pass the needed information to the template rendering
    dot_syntax = template.render()

    #  Sending the diagram to kroki.io to get the SVG
    #  We could also use the kroki get url with the encoded diagram
    try:
        response = requests.post("https://kroki.io/graphviz/svg/", data=dot_syntax)
        response.raise_for_status()
        with output.open("w") as fp:
            fp.write(response.text)
    except requests.HTTPError as exc:
        typer.echo(f"Error: {exc}", err=True)
        typer.echo("Generating SVG failed", err=True)
        raise typer.Exit(1)

    typer.echo("You can use the following URL to view the diagram in the browser:")
    typer.echo(_kroki_get_url("https://kroki.io/graphviz/svg/", dot_syntax))


@app.command()
def d2(ctx: typer.Context, output: Path = "d2.svg") -> None:
    """
    Visualize the topology with D2
    """
    #  TODO: Like GraphViz but with D2


if __name__ == "__main__":
    app()
