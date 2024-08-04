from config import con, cur


class PostFunctions:
    @staticmethod
    def post_data(spn, coords, display, pt, z, postal_code, address, checkboxIndex, searchInfo):
        req = """
            UPDATE maps SET spn = ?, coords = ?, display = ?, pt = ?, z = ?, postal_code = ?, address = ?,
            checkbox_index = ?, search_info = ? 
            WHERE id = 1
        """
        cur.execute(
            req, (spn, f"{coords[0]}, {coords[1]}", display, pt, z, postal_code, address, checkboxIndex, searchInfo)
        )
        con.commit()
