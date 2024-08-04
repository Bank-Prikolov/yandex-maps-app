import os

from config import cur, con


def terminate():
    os.remove('assets/general/map.png')
    cur.close()
    con.close()
