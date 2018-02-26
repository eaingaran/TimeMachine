import sqlite3


def get_connection(database):
    return sqlite3.connect(database)
