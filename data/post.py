from config import con, cur


class Post:
    @staticmethod
    def post_data(lang, spn, coords, display, pt, z, postal_code, address, checkboxIndex, searchInfo):
        req = """
            UPDATE maps SET lang = ?, spn = ?, coords = ?, display = ?, pt = ?, z = ?, postal_code = ?, address = ?,
            checkbox_index = ?, search_info = ? 
            WHERE id = 1
        """
        cur.execute(
            req,
            (lang, spn, f"{coords[0]}, {coords[1]}", display, pt, z, postal_code, address, checkboxIndex, searchInfo)
        )
        con.commit()
