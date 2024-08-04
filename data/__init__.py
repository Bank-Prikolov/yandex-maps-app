from dataclasses import dataclass, field

from .get import GetFunctions
from .post import PostFunctions
from .tables import Tables


Tables.create_tables()


@dataclass
class MapsData:
    spn: float = GetFunctions.get_spn()
    coords: list = field(default_factory=lambda: list(GetFunctions.get_coords()))
    display: str = GetFunctions.get_display()
    pt: str = GetFunctions.get_pt()
    postal_code: str = GetFunctions.get_postal_code()
    address: str = GetFunctions.get_address()
    z: int = GetFunctions.get_zoom()
    checkbox_index: int = GetFunctions.get_checkbox_index()
    search_info: str = GetFunctions.get_search_info()

    @staticmethod
    def post_data(spn, coords, display, pt, z, postal_code, address, checkboxIndex, searchInfo):
        PostFunctions.post_data(spn, coords, display, pt, z, postal_code, address, checkboxIndex, searchInfo)
