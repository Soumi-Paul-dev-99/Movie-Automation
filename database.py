
import sqlite3

DB_NAME = "movieDB.sqlite3"


def create_database():

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    # Movie Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Movie(
            movie_id INTEGER PRIMARY KEY,
            genre TEXT,
            time TEXT
        )
    """)

    # Hall Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Hall(
            hall_id INTEGER PRIMARY KEY,
            movie_id INTEGER,
            FOREIGN KEY(movie_id) REFERENCES Movie(movie_id)
        )
    """)

    # Multiplex Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Multiplex(
            multiplex_id INTEGER,
            movie_id INTEGER,
            hall_id INTEGER,
            PRIMARY KEY(multiplex_id, hall_id),
            FOREIGN KEY(movie_id) REFERENCES Movie(movie_id),
            FOREIGN KEY(hall_id) REFERENCES Hall(hall_id)
        )
    """)

    # Insert Movie Data
    cur.executemany("""
        INSERT OR IGNORE INTO Movie
        (movie_id, genre, time)
        VALUES (?, ?, ?)
    """, [
        (1, "Action", "2h 30m"),
        (2, "Comedy", "2h"),
        (3, "Romance", "2h 15m"),
        (4, "Thriller", "2h 20m")
    ])

    # Insert Hall Data
    cur.executemany("""
        INSERT OR IGNORE INTO Hall
        (hall_id, movie_id)
        VALUES (?, ?)
    """, [
        (101, 1),
        (102, 2),
        (103, 3),
        (104, 4)
    ])

    # Insert Multiplex Data
    cur.executemany("""
        INSERT OR IGNORE INTO Multiplex
        (multiplex_id, movie_id, hall_id)
        VALUES (?, ?, ?)
    """, [
        (1, 1, 101),
        (1, 2, 102),
        (2, 3, 103),
        (2, 4, 104)
    ])

    con.commit()
    con.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()
