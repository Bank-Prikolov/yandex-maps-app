from config import cur


class GetFunctions:
    @staticmethod
    def get_spn():
        req = """
            SELECT spn 
            FROM maps
            WHERE id = 1
        """
        result = float(cur.execute(req).fetchone()[0])
        return result

    @staticmethod
    def get_coords():
        req = """
            SELECT coords
            FROM maps
            WHERE id = 1
        """
        result = cur.execute(req).fetchone()[0].split(', ')
        return float(result[0]), float(result[1])

    @staticmethod
    def get_display():
        req = """
            SELECT display 
            FROM maps 
            WHERE id = 1
        """
        result = cur.execute(req).fetchone()[0]
        return result

    @staticmethod
    def get_pt():
        req = """
            SELECT pt 
            FROM maps 
            WHERE id = 1
        """
        result = cur.execute(req).fetchone()[0]
        return result

    @staticmethod
    def get_zoom():
        req = """
            SELECT z
            FROM maps
            WHERE id = 1
        """
        result = int(cur.execute(req).fetchone()[0])
        return result

    @staticmethod
    def get_postal_code():
        req = """
            SELECT postal_code 
            FROM maps 
            WHERE id = 1
        """
        result = cur.execute(req).fetchone()[0]
        return result

    @staticmethod
    def get_address():
        req = """
            SELECT address 
            FROM maps 
            WHERE id = 1
        """
        result = cur.execute(req).fetchone()[0]
        return result

    @staticmethod
    def get_checkbox_index():
        req = """
            SELECT checkbox_index
            FROM maps 
            WHERE id = 1
        """
        result = int(cur.execute(req).fetchone()[0])
        return result

    @staticmethod
    def get_search_info():
        req = """
            SELECT search_info 
            FROM maps 
            WHERE id = 1
        """
        result = cur.execute(req).fetchone()[0]
        return result
