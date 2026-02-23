import os
import sqlite3
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import create_tables, DB_NAME


def test_database_tables_exist():
    # create tables
    create_tables()

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # check stations table
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stations'")
    assert cur.fetchone() is not None

    # check measurements table
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='measurements'")
    assert cur.fetchone() is not None

    conn.close()