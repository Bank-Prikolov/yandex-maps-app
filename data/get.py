from config import cur


class GetFunction:
    @staticmethod
    def get_data():
        req = """
            SELECT *
            FROM maps
            WHERE id = 1
        """
        result = list(cur.execute(req).fetchone())
        return result
