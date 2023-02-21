# pylint: disable=redefined-builtin, too-many-arguments
# pylint: disable=duplicate-code
"""
This module contains the song commands
"""
from pathlib import Path
import sys
import typer
from rich.console import Console
from rich.table import Table
from db import get_query, query_db

console = Console()

app = typer.Typer(name="song", help="Query songs in the database")
path = Path("./database.db")


@app.command()
def list(
    limit: int = typer.Option(10, help="Limit the results to a specific number"),
    title: str = typer.Option(None, help="Filter by song title"),
    streams: str = typer.Option(None, help="Filter by number of streams in billions"),
    artist: str = typer.Option(None, help="Filter by artist name"),
    year: str = typer.Option(None, help="Filter by release year"),
    rank: str = typer.Option(None, help="Filter by rank"),
):
    """
    [bold green]List[/bold green] songs in the database
    """

    params = {
        "title": title,
        "streams": streams,
        "artist": artist,
        "year": year,
        "rank": rank,
    }
    new_params = {}
    for k, value in params.items():
        if value is not None:
            value = value.strip()
        new_params[k] = value
    query = get_query(
        {
            "table": "songs",
            "params": new_params,
            "limit": limit,
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
            "Title",
            "Streams (Billions)",
            "Artist",
            "Release Date",
            header_style="bold blue",
        )
        for result in results:
            row = [str(result[0]), result[1], str(result[2]), result[3], str(result[4])]
            table.add_row(*row)
        console.print(table)


@app.command()
def metadata():
    """
    Shows [bold blue]metadata[/bold blue] about the songs table
    """

    query = "PRAGMA table_info(artists);"
    table_size_query = "SELECT COUNT(*) FROM songs;"

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
        console.print("This data was pulled from kaggle. The data was last updated December 2022")


if __name__ == "__main__":
    app()
