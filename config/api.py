from dataclasses import dataclass
import os
from dotenv import load_dotenv


load_dotenv()


@dataclass
class YandexApisConfig:
    GEOCODE_API_KEY: str = os.getenv('GEOCODE_API_KEY')
    SEARCH_API_KEY: str = os.getenv('SEARCH_API_KEY')
