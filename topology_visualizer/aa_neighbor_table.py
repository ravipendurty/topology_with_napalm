from typing import Dict, List, Union

import typer
from napalm import get_network_driver

from rich.console import Console
from rich.table import Table

app = typer.Typer(
    help="Generate Rich Neighbor Table for a device",
    rich_markup_mode="rich",
    add_completion=False,
)


def _create_table(
    device_name: str, lldp_data: Dict[str, List[Dict[str, Union[str, List[str]]]]]
) -> Table:
    table = Table(title=f"Neighbor Table: [b]{device_name}[/b]")
    table.add_column("Interface", style="green")
    table.add_column("Remote System Name", justify="right")
    table.add_column("Remote System Interface")

    # TODO: Populate the rich table with the LLDP data from the device
    for key in lldp_data:
        #print (key, "->", lldp_data[key])
        lldp_details_list = lldp_data[key]
        length =  len(lldp_details_list)
        for i in range(length):
            #print(lldp_details_list[i])
            table.add_row(key, lldp_details_list[i]["remote_system_name"], lldp_details_list[i]["remote_port"])

    return table


@app.command(no_args_is_help=True)
def neighbor_table(
    ctx: typer.Context,
    device_name: str,
) -> None:
    """
    Collect the LLDP neighbor details with NAPALM

    For example, the following table is generated if you provide the device name [b]che01[/b].

                      [i]Neighbor Table: [b]che01[/b][/i]
    | Interface  | Remote System Name | Remote System Interface |
    | ---------- | ------------------ | ----------------------- |
    | Ethernet1  |              deu01 | Ethernet2               |
    | Ethernet2  |              ita01 | Ethernet1               |
    | Ethernet3  |              fra02 | Ethernet2               |
    | Ethernet4  |              fra01 | Ethernet4               |
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

    console = Console()
    console.print(_create_table(device_name, lldp_data))


if __name__ == "__main__":
    app()
