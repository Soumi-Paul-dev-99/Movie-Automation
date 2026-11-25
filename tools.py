
import sqlite3

DB_NAME = "movieDB.sqlite3"


# 1. Show all movies
def show_all_movies():

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute("""
        SELECT movie_id, genre, time
        FROM Movie
    """)

    data = cur.fetchall()
    con.close()

    if not data:
        return "No movies found."

    result = "All Movies:\n"

    for row in data:
        result += f"""
        Movie ID: {row[0]}
        Genre: {row[1]}
        Time: {row[2]}
        ------------------
        """

    return result


# 2. Show movies by multiplex
def show_movies_by_multiplex(multiplex_id: int):

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute("""
        SELECT DISTINCT
            m.movie_id,
            m.genre,
            m.time
        FROM Multiplex mx
        JOIN Movie m ON mx.movie_id = m.movie_id
        WHERE mx.multiplex_id = ?
    """, (multiplex_id,))

    data = cur.fetchall()
    con.close()

    if not data:
        return "No movies found in this multiplex."

    result = f"Movies in Multiplex {multiplex_id}:\n"

    for row in data:
        result += f"""
        Movie ID: {row[0]}
        Genre: {row[1]}
        Time: {row[2]}
        ------------------
        """

    return result


# 3. Show halls by multiplex
def show_halls_by_multiplex(multiplex_id: int):

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute("""
        SELECT DISTINCT hall_id
        FROM Multiplex
        WHERE multiplex_id = ?
    """, (multiplex_id,))

    data = cur.fetchall()
    con.close()

    if not data:
        return "No halls found in this multiplex."

    result = f"Halls in Multiplex {multiplex_id}:\n"

    for row in data:
        result += f"Hall ID: {row[0]}\n"

    return result


# 4. Show movie details by multiplex and hall
def show_movie_details(multiplex_id: int, hall_id: int):

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute("""
        SELECT
            mx.multiplex_id,
            h.hall_id,
            m.movie_id,
            m.genre,
            m.time
        FROM Multiplex mx
        JOIN Hall h
            ON mx.hall_id = h.hall_id
            AND mx.movie_id = h.movie_id
        JOIN Movie m
            ON mx.movie_id = m.movie_id
        WHERE mx.multiplex_id = ?
        AND mx.hall_id = ?
    """, (multiplex_id, hall_id))

    data = cur.fetchall()
    con.close()

    if not data:
        return "No movie details found for this multiplex and hall."

    result = "Movie Details:\n"

    for row in data:
        result += f"""
        Multiplex ID: {row[0]}
        Hall ID: {row[1]}
        Movie ID: {row[2]}
        Genre: {row[3]}
        Time: {row[4]}
        ------------------
        """

    return result
