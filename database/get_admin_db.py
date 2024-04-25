import sqlite3
from database import update_db


def add_id(user_id):
    con = sqlite3.connect("../database/school_db.sqlite")
    cur = con.cursor()
    result = cur.execute(f"""INSERT INTO admins_chat_id VALUES ({user_id});""").fetchall()
    con.commit()
    cur.close()
    update_db.db_updating()
