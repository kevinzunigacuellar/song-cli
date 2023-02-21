"""
This module contains the artist commands
"""
# pylint: disable=duplicate-code
from pathlib import Path
import sys
import typer
from rich.console import Console
from rich.table import Table
from db import get_query, query_db


console = Console()
app = typer.Typer(name="artist", help="Query artists in the database")
path = Path("./database.db")


@app.command()
# pylint: disable=redefined-builtin
def list(
    limit: int = typer.Option(10, help="Limit the results to a specific number"),
    name: str = typer.Option(None, help="Filter by artist name"),
    streams: str = typer.Option(None, help="Filter by number of streams in billions"),
    rank: str = typer.Option(None, help="Filter by rank"),
    tracks: str = typer.Option(None, help="Filter by number of tracks"),
):
    """
    [bold green]List[/bold green] artists in the database
    """
    params = {"name": name.strip(), "streams": streams, "rank": rank, "tracks": tracks}
    query = get_query(
        {
            "limit": limit,
            "table": "artists",
            "params": params,
        }
    )

    if path.is_file() is True:
        results = query_db(query)
    else:
        console.print(
            "Data not found, please run [black on magenta] cli load [/black on magenta] first",
        )
        sys.exit(0)

    if len(results) == 0:
        console.print("No results found :sob:")
    else:
        table = Table(
            "Rank",
            "Name",
            "Streams (Billions)",
            "Number of tracks",
            header_style="bold blue",
        )
        for result in results:
            row = [str(result[0]), result[1], str(result[2]), str(result[3])]
            table.add_row(*row)
        console.print(table)


@app.command()
def metadata():
    """
    Shows [bold blue]metadata[/bold blue] about the artists table
    """

    query = "PRAGMA table_info(artists);"
    table_size_query = "SELECT COUNT(*) FROM artists;"

    if path.is_file() is True:
        results = query_db(query)
        table_size = query_db(table_size_query)
    else:
        console.print(
            "Data not found, please run [black on magenta] cli load [/black on magenta] first",
        )
        sys.exit(0)

    if len(results) == 0:
        console.print("No results found :sob:")

    else:
        table = Table(
            "Column ID",
            "Name",
            "Type",
            "Not Null",
            "Default Value",
            "Primary Key",
            header_style="bold blue",
        )
        for result in results:
            row = [
                str(result[0]),
                result[1],
                result[2],
                str(result[3]),
                result[4],
                str(result[5]),
            ]
            table.add_row(*row)
        console.print(table)
        console.print(f"Table size: {table_size[0][0]} rows")
        console.print("This data was pulled from kaggle, pulled directly from spotify.")
        console.print("The data was last updated December 2022")

if __name__ == "__main__":
    app()
