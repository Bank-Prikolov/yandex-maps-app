import sqlite3

con = sqlite3.connect("data/db.sqlite")
cur = con.cursor()


def firstTime():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        lastData(levelID INT PRIMARY KEY, isPassing INT, record INT, time INT, lastRecord INT, lastTime INT)
        """)
    con.commit()
