import sqlite3
import os
import sys


def start_db() -> sqlite3.Connection:
    HERE = os.path.dirname(sys.argv[0])
    conn = sqlite3.connect(os.path.join(HERE, "scraped_text.db"))

    # Create db if not exists
    c = conn.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imgur_id TEXT UNIQUE,
        img_path TEXT,
        text TEXT
    );
    """
    )
    conn.commit()

    return conn


def insert_text(
    conn: sqlite3.Connection, imgur_id: str, img_path: str, text: str
) -> int:
    c = conn.cursor()
    sql = "INSERT OR IGNORE INTO texts (imgur_id, img_path, text) VALUES (?,?,?);"
    vals = (imgur_id, img_path, text)
    id = c.execute(sql, vals).lastrowid
    conn.commit()
    return id


def image_already_scraped(conn: sqlite3.Connection, imgur_id: str) -> bool:
    c = conn.cursor()
    sql = "SELECT * FROM texts WHERE imgur_id = ?;"
    vals = (imgur_id,)
    c.execute(sql, vals)
    return c.fetchone() is not None


def get_new_images_from_path_list(
    conn: sqlite3.Connection, path_list: list
) -> list[tuple]:
    """
    Get a list of image paths, from their imgur_ids, return a
    list of image paths that are not already in the database.
    """
    # Create list with all image ids
    imgur_ids = [path.split("/")[-1].split(".")[0] for path in path_list]
    # Add ' ' around each id to pass it to the select query
    imgur_ids = ["'" + id + "'" for id in imgur_ids]

    # Get the imgur_ids from the database that ARE in the imgur_ids
    # Doing with fstring since I couldn't make it work properly with VALS
    sql = f"SELECT imgur_id FROM texts WHERE imgur_id IN ({','.join(imgur_ids)});"

    c = conn.cursor()
    c.execute(sql)

    # Get a list of the ids and then filter the original path_list to get the ones that are not in the database
    already_scraped = [id[0] for id in c.fetchall()]
    return [
        path
        for path in path_list
        if path.split("/")[-1].split(".")[0] not in already_scraped
    ]


def get_all_images_with_text(conn: sqlite3.Connection) -> list[tuple]:
    c = conn.cursor()
    sql = "SELECT * FROM texts WHERE text IS NOT NULL;"
    c.execute(sql)
    return c.fetchall()
