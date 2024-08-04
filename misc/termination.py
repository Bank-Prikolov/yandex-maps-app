import os

from config import con, cur


def terminate():
    os.remove('assets/general/map.png')
    cur.close()
    con.close()
