import sqlite3


def schedule_printing(number, letter):
    con = sqlite3.connect("../database/school_db.sqlite")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM schedule WHERE (number = {number}) AND (letter = '{letter}'); """).fetchall()
    cur.close()
    con.close()
    return result
