import sqlite3

con = sqlite3.connect("data/db.sqlite")
cur = con.cursor()


def firstTime():
    cur.execute("""
            CREATE TABLE IF NOT EXISTS
            MapsData(id INT PRIMARY KEY, spn REAL, coords TEXT, display TEXT, pt TEXT, postal_code TEXT, address TEXT)
        """)
    cur.execute("""
            INSERT INTO MapsData (id, spn, coords, display, pt, postal_code, address) 
            VALUES (1, 0.003, '32.095323, 54.769680', 'map', '', '', '')
            ON CONFLICT (id) DO NOTHING
        """)
    con.commit()


def get_spn():
    req = f"""SELECT spn FROM MapsData WHERE id = 1"""
    result = float(cur.execute(req).fetchone()[0])
    return result


def get_coords():
    req = f"""SELECT coords FROM MapsData WHERE id = 1"""
    result = cur.execute(req).fetchone()[0].split(', ')
    return result[0], result[1]


def get_display():
    req = f"""SELECT display FROM MapsData WHERE id = 1"""
    result = cur.execute(req).fetchone()[0]
    return result


def get_pt():
    req = f"""SELECT pt FROM MapsData WHERE id = 1"""
    result = cur.execute(req).fetchone()[0]
    return result


def get_postal_code():
    req = f"""SELECT postal_code FROM MapsData WHERE id = 1"""
    result = cur.execute(req).fetchone()[0]
    return result


def get_address():
    req = f"""SELECT address FROM MapsData WHERE id = 1"""
    result = cur.execute(req).fetchone()[0]
    return result
