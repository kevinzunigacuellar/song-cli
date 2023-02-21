"""
This module starts the CLI
"""
# pylint: disable=line-too-long
import sys
from pathlib import Path
import typer
from rich import print as p_print
import song
import artist
from db import create_tables, load_data, query_db

path = Path("./database.db")

app = typer.Typer(help="Awesome music database CLI :sparkles:", rich_markup_mode="rich")
app.add_typer(song.app, name="song")
app.add_typer(artist.app, name="artist")


@app.command()
def load():
    """
    Load data into the database
    """
    p_print("[bold blue]Creating database ...[/bold blue]")
    create_tables()
    p_print("[bold green]:white_check_mark: Tables created[/bold green]")
    load_data()
    p_print("[bold green]:white_check_mark: Data loaded[/bold green]")


@app.command()
def peak_song(rank: int = typer.Argument(1, help="Artist rank")):
    """
    Get the highest ranked song using the artist rank
    """
    query = f"SELECT artist,title, rank FROM songs WHERE rank = (SELECT MIN(rank) FROM songs WHERE artist = (SELECT name FROM artists WHERE rank = {rank}));"

    if path.is_file() is True:
        results = query_db(query)
    else:
        p_print(
            "Data not found, please run [black on magenta] cli load [/black on magenta] first",
        )
        sys.exit(0)

    if len(results) == 0:
        p_print("No results found :sob:")
    else:
        p_print(
            f"The highest ranked song for the artist with rank {rank}, [green]{results[0][0]}[/green], is [bold blue]{results[0][1]}[/bold blue], at rank [bold blue]{results[0][2]}[/bold blue]"
        )


if __name__ == "__main__":
    app()
