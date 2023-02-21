"""Database module"""

import sqlite3
import pandas as pd

SONGS_FILE = "src/data/songs.csv"
ARTISTS_FILE = "src/data/artists.csv"
DATABASE_NAME = "database.db"


def create_tables():
    """Create tables in database"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.executescript(
            """
            DROP TABLE IF EXISTS songs;
            DROP TABLE IF EXISTS artists;

            CREATE TABLE songs
        (
            rank INT,
            title TEXT,
            streams INT,
            artist TEXT,
            release_date DATE,
            PRIMARY KEY(rank),
            FOREIGN KEY(artist) REFERENCES artists(name)
        );
            CREATE TABLE artists
        (
            rank INT,
            name TEXT,
            streams INT,
            tracks INT,
            PRIMARY KEY(rank),
            FOREIGN KEY(name) REFERENCES songs(artist)
        );
        """
        )
        conn.commit()

    except sqlite3.DatabaseError:
        print("Error, could not create tables.")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def load_data():
    """Load csv files into database"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        songs = pd.read_csv(SONGS_FILE)
        artists = pd.read_csv(ARTISTS_FILE)
        songs["release_date"] = pd.to_datetime(songs["release_date"])
        songs.to_sql("songs", conn, if_exists="replace", index=False)
        artists.to_sql("artists", conn, if_exists="replace", index=False)
        conn.commit()

    except sqlite3.DatabaseError:
        print("Error, could not load data.")
    finally:
        if conn is not None:
            conn.close()


def get_query(args: dict) -> str:
    """Construct and return the query"""
    query = f"SELECT * FROM {args['table']}"

    # remove None values from params
    args["params"] = {k: v for k, v in args["params"].items() if v is not None}

    if args["params"].items() is not None:
        query += " WHERE "
        for key, value in args["params"].items():
            if key in ["streams", "tracks", "rank"]:
                if value.startswith(">"):
                    query += f"{key} > {value[1:]}"
                elif value.startswith("<"):
                    query += f"{key} < {value[1:]}"
                else:
                    query += f"{key} = {value}"
            if key in ["name", "artist", "title"]:
                query += f"{key} LIKE '%{value}%'"
            if key == "year":
                if value.startswith(">"):
                    query += f"release_date > '{value[1:]}-01-01'"
                elif value.startswith("<"):
                    query += f"release_date < '{value[1:]}-01-01'"
                else:
                    query += f"release_date BETWEEN '{value}-01-01' AND '{value}-12-31'"
            query += " AND "
        query = query[:-5]  # Remove extra AND
    query += f" LIMIT {args['limit']}"
    return query


def query_db(query: str) -> list | None:
    """Query the database here and return the results"""

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except sqlite3.DatabaseError:
        print("Error, could not list songs.")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
