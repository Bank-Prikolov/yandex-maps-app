import sqlite3

con = sqlite3.connect("data/db.sqlite")
cur = con.cursor()


def firstTime():
    cur.execute("""
            CREATE TABLE IF NOT EXISTS
            MapsData(id INT PRIMARY KEY, spn REAL, coords TEXT, display TEXT, pt TEXT, postal_code TEXT, address TEXT, 
            checkboxIndex INT, searchInfo TEXT)
        """)
    cur.execute("""
            INSERT INTO MapsData (id, spn, coords, display, pt, postal_code, address, checkboxIndex, searchInfo) 
            VALUES (1, 0.003, '32.095323, 54.769680', 'map', '', '', '', 0, '')
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
    return float(result[0]), float(result[1])


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


def get_checkbox_index():
    req = f"""SELECT checkboxIndex FROM MapsData WHERE id = 1"""
    result = cur.execute(req).fetchone()[0]
    return int(result)


def get_search_info():
    req = f"""SELECT searchInfo FROM MapsData WHERE id = 1"""
    result = cur.execute(req).fetchone()[0]
    return result


def write_data(spn, coords, display, pt, postal_code, address, checkboxIndex, searchInfo):
    cur.execute(f"""UPDATE MapsData SET spn = {spn}, coords = '{coords[0]}, {coords[1]}', display = '{display}', 
    pt = '{pt}', postal_code = '{postal_code}', address = '{address}', checkboxIndex = {checkboxIndex}, 
    searchInfo = '{searchInfo}' WHERE id = 1""")
    con.commit()
