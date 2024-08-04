import os

from config import con


def terminate():
    os.remove('assets/images/map.png')
    con.close()
