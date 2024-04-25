import sqlite3


def get_all_news():
    con = sqlite3.connect("../database/school_db.sqlite")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM news; """).fetchall()
    cur.close()
    con.close()
    return result
