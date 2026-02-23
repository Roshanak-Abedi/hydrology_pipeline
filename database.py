import sqlite3

DB_NAME = "data/hydrology.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # FACT table (stations as central fact-like table)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        station_id TEXT PRIMARY KEY,
        name TEXT,
        river TEXT,
        latitude REAL,
        longitude REAL
    )
    """)

    # measurement table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS measurements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id TEXT,
        parameter TEXT,
        datetime TEXT,
        value REAL,
        unit TEXT,
        FOREIGN KEY (station_id) REFERENCES stations(station_id),
        UNIQUE (station_id, parameter, datetime)
            
            )
    """)

    conn.commit()
    conn.close()


def insert_station(station):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO stations
    VALUES (?, ?, ?, ?, ?)
    """, (
        station["notation"],
        station["label"],
        station.get("riverName"),
        station.get("lat"),
        station.get("long")
    ))

    conn.commit()
    conn.close()


def insert_measurements(station_id, parameter, unit, readings):
    conn = get_connection()
    cur = conn.cursor()

    rows = [
        (station_id, parameter, r["dateTime"], r["value"], unit)
        for r in readings
    ]

    cur.executemany("""
    INSERT OR IGNORE INTO measurements
    (station_id, parameter, datetime, value, unit)
    VALUES (?, ?, ?, ?, ?)
    """, rows)


    conn.commit()
    conn.close()