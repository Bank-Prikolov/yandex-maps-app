from config import con, cur


class Tables:
    @staticmethod
    def create_tables():
        cur.execute("""
                CREATE TABLE IF NOT EXISTS
                maps(
                id INT PRIMARY KEY, lang TEXT, spn REAL, coords TEXT, display TEXT, pt TEXT, z INT, postal_code TEXT, 
                address TEXT, checkbox_index INT, search_info TEXT)
            """)
        cur.execute("""
                INSERT 
                INTO maps (id, lang, spn, coords, display, pt, z, postal_code, address, checkbox_index, search_info) 
                VALUES (1, 'ru', 0.003, '32.095323, 54.769680', 'map', '', 16, '', '', 0, '')
                ON CONFLICT (id) DO NOTHING
            """)
        con.commit()
