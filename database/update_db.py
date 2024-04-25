import sqlite3


def db_updating():
    con = sqlite3.connect("../database/school_db.sqlite")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM schedule """).fetchall()
    cur.close()
    con.close()
    return result
