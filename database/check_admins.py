import sqlite3


def check_admins():
    con = sqlite3.connect("../database/school_db.sqlite")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM admins_chat_id; """).fetchall()
    cur.close()
    con.close()
    return result
