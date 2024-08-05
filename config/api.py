from dataclasses import dataclass
import os
from dotenv import load_dotenv


load_dotenv()


@dataclass
class YandexApisConfig:
    GEOCODER_API_KEY: str = os.getenv('GEOCODER_API_KEY')
    PLACES_API_KEY: str = os.getenv('PLACES_API_KEY')
