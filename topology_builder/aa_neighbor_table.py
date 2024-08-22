import typer
from napalm import get_network_driver

from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Generate Rich Neighbor Tabel for a device")


@app.command()
def neighbor_table(
    ctx: typer.Context,
    device_name: str,
) -> None:
    """
    Collect the LLDP neighbor details with NAPALM
    
    Provide a device name like "che01"
    """
    try:
        driver = get_network_driver("mock")
        with driver(
            device_name,
            "username",  # Mandatory but not used by the mock driver
            "password",  # Mandatory but not used by the mock driver
            optional_args={"path": f"mocked_napalm_data/{device_name}"},
        ) as device:
            lldp_data = device.get_lldp_neighbors_detail()

    except NotImplementedError as exc:
        # The napalm mock driver throws a NotImplementedError exception when the file is not found.
        # This is only needed because we use the mock driver
        typer.echo(f"Error: {exc}", err=True)
        typer.echo("Did you enter a valid device name?", err=True)
        raise typer.Exit(1)

    table = Table(title=f"Neighbor Table: [b]{device_name}[/]")
    table.add_column("Interface", style="green")
    table.add_column("Remote System Name", justify="right")
    table.add_column("Remote System Interface")

    # TODO: Populate the rich table with the LLDP data from the device

    console = Console()
    console.print(table)


if __name__ == "__main__":
    app()
