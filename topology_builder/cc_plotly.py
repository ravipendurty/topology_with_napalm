from pathlib import Path

import typer
import plotly.graph_objects as go

app = typer.Typer(
    help="Visualize the topology with a GeoMap",
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


@app.command()
def geomap(
    ctx: typer.Context,
    svg_output: Path = "plotly.svg",
    html_output: Path = "plotly.html",
) -> None:
    """
    Visualize the topology with a GeoMap
    """
    try:
        _get_topology()

    except TopologyError as exc:
        typer.echo(f"Error: {exc}", err=True)
        typer.echo("Collecting the topology failed", err=True)
        raise typer.Exit(1)

    fig = go.Figure()

    #  TODO: Point all routers
    fig.add_trace(
        go.Scattergeo(
            lon=[6.143158, 9.1859243],
            lat=[46.204391, 45.4654219],
            text=["che01 (Geneva)", "ita01 (Milan)"],
            mode="markers",
            marker={
                "size": 7,
                "color": "rgb(255, 0, 0)",
                "line": {
                    "width": 3,
                    "color": "rgba(68, 68, 68, 0)",
                },
            },
        )
    )

    #  TODO: add all links (this is the link between che01 and ita01)
    fig.add_trace(
        go.Scattergeo(
            lon=[6.143158, 9.1859243],
            lat=[46.204391, 45.4654219],
            mode="lines",
            line={"width": 1, "color": "red"},
        )
    )

    fig.update_layout(
        title_text="Network Topology<br>Europe",
        showlegend=False,
        geo={
            "scope": "europe",
            "projection_type": "azimuthal equal area",
            "showland": True,
            "landcolor": "rgb(243, 243, 243)",
            "countrycolor": "rgb(204, 204, 204)",
        },
    )
    fig.write_html(html_output)
    fig.write_image(svg_output)


if __name__ == "__main__":
    app()
