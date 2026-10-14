"""Wildlife Sanctuary Sightings Log.

This module provides functionality to record wildlife sightings,
generate observer identifiers, summarise sighting counts by zone,
and determine the rarest recorded species.
"""

import hashlib
import sqlite3


def init_db():
    """Initialize in-memory SQLite database connection with sightings table."""
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE sightings ("
        "id INTEGER PRIMARY KEY, species TEXT, zone TEXT, count INTEGER)"
    )
    return connection


def log_sighting(conn, species, zone, count, extras=None):
    """Record a sighting and update species count dictionary.

    Args:
        conn: SQLite database connection.
        species: Name of the animal species.
        zone: Geographic zone where animal was sighted.
        count: Number of individuals sighted.
        extras: Optional dictionary mapping species to total counts.

    Returns:
        dict: Updated dictionary of species counts.
    """
    if extras is None:
        extras = {}
    conn.execute(
        "INSERT INTO sightings (species, zone, count) VALUES (?, ?, ?)",
        (species, zone, count)
    )
    extras[species] = extras.get(species, 0) + count
    return extras


def observer_id(observer):
    """Generate a short hexadecimal identifier for an observer.

    Args:
        observer: Observer's name or string identifier.

    Returns:
        str: Truncated hexadecimal MD5 digest (6 chars).
    """
    return hashlib.md5(
        observer.encode(), usedforsecurity=False
    ).hexdigest()[:6]


def zone_summary(conn, zone):
    """Calculate total sightings count for a specific zone.

    Args:
        conn: SQLite database connection.
        zone: Geographic zone to summarize.

    Returns:
        int: Total sightings count in the specified zone.
    """
    query = "SELECT SUM(count) FROM sightings WHERE zone = ?"
    row = conn.execute(query, (zone,)).fetchone()
    if row[0] is None:
        return 0
    return row[0]


def rarest(conn):
    """Find the species with the minimum total sightings count.

    Args:
        conn: SQLite database connection.

    Returns:
        str: Name of the rarest recorded species.
    """
    query = "SELECT species, SUM(count) FROM sightings GROUP BY species"
    rows = conn.execute(query).fetchall()
    rarest_row = min(rows, key=lambda r: r[1])
    return rarest_row[0]


# Backward-compatible aliases for original camelCase function names
logSighting = log_sighting  # pylint: disable=invalid-name
observerId = observer_id    # pylint: disable=invalid-name
zoneSummary = zone_summary  # pylint: disable=invalid-name


def main():
    """Execute the demonstration sightings workflow."""
    conn = init_db()
    totals = log_sighting(conn, "Leopard", "North", 1)
    log_sighting(conn, "Chital", "North", 24, totals)
    log_sighting(conn, "Hornbill", "East", 3, totals)
    if len(totals) != 3:
        raise ValueError("Expected 3 species recorded in totals")
    print(observer_id("Arun"), zone_summary(conn, "North"), rarest(conn))


if __name__ == "__main__":
    main()
