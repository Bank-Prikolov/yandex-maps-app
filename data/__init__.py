from dataclasses import dataclass, field

from .get import GetFunction
from .post import PostFunction
from .tables import Tables


Tables.create_tables()
data = GetFunction.get_data()


@dataclass
class MapsData:
    lang: str = data[1]
    spn: float = data[2]
    coords: list = field(default_factory=lambda: list(map(float, data[3].split(', '))))
    display: str = data[4]
    pt: str = data[5]
    z: int = data[6]
    postal_code: str = data[7]
    address: str = data[8]
    checkbox_index: int = data[9]
    search_info: str = data[10]

    @staticmethod
    def post_data(lang, spn, coords, display, pt, z, postal_code, address, checkbox_index, search_info):
        PostFunction.post_data(lang, spn, coords, display, pt, z, postal_code, address, checkbox_index, search_info)
