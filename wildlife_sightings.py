import hashlib
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE sightings ("
    "id INTEGER PRIMARY KEY, species TEXT, zone TEXT, count INTEGER)"
)


def logSighting(conn, species, zone, count, extras={}):
    conn.execute(
        "INSERT INTO sightings (species, zone, count) VALUES (?, ?, ?)",
        (species, zone, count)
    )
    extras[species] = extras.get(species, 0) + count
    return extras


def observerId(observer):
    return hashlib.md5(
        observer.encode(), usedforsecurity=False
    ).hexdigest()[:6]


def zoneSummary(conn, zone):
    query = "SELECT SUM(count) FROM sightings WHERE zone = ?"
    row = conn.execute(query, (zone,)).fetchone()
    if row[0] is None:
        return 0
    else:
        return row[0]


def rarest(conn):
    query = "SELECT species, SUM(count) FROM sightings GROUP BY species"
    rows = conn.execute(query).fetchall()
    rarest_row = min(rows, key=lambda r: r[1])
    return rarest_row[0]


def main():
    totals = logSighting(conn, "Leopard", "North", 1)
    logSighting(conn, "Chital", "North", 24, totals)
    logSighting(conn, "Hornbill", "East", 3, totals)
    if len(totals) != 3:
        raise ValueError("Expected 3 species recorded in totals")
    print(observerId("Arun"), zoneSummary(conn, "North"), rarest(conn))


main()
