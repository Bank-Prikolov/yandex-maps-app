from config import cur


class Get:
    @staticmethod
    def get_data():
        req = """
            SELECT *
            FROM maps
            WHERE id = 1
        """
        result = list(cur.execute(req).fetchone())
        return result
