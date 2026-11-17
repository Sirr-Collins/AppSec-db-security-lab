#
# import sqlite3
# from pathlib import Path
#
# DATABASE_PATH = Path(__file__).parent / "instance" / "app.db"
#
#
# def get_connection():
#     DATABASE_PATH.parent.mkdir(exist_ok=True)
#
#     connection = sqlite3.connect(DATABASE_PATH)
#     connection.row_factory = sqlite3.Row
#
#     return connection


import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "instance" / "app.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


