import sqlite3

conn = sqlite3.connect("data/hydrology.db")
cur = conn.cursor()

print("\n--- Stations ---")
for row in cur.execute("SELECT * FROM stations"):
    print(row)

print("\n--- Measurements (last 5) ---")
for row in cur.execute("SELECT *  FROM measurements order by datetime  DESC limit 5"):
    print(row)
 
print("\n--- Measurement Count by Parameter ---")
for row in cur.execute("SELECT parameter, COUNT(*) FROM measurements GROUP BY parameter"):
    print(row)

print("\n--- Measurement Count/check if inserted duplicate ---")
for row in cur.execute("SELECT COUNT(*) FROM measurements"):
    print(row)

print("\n--- Latest measurement timestamp ---")
latest_dt = cur.execute("SELECT MAX(datetime) FROM measurements").fetchone()[0]
print(latest_dt)

conn.close()


