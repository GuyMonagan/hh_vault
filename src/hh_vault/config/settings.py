import os
from dotenv import load_dotenv

load_dotenv()

HH_API_URL = os.getenv("HH_API_URL", "https://api.hh.ru")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

COMPANY_IDS = [
    1740,     # Яндекс
    3529,     # Сбер
    2748,     # Тинькофф
    1455,     # Газпром
    78638,    # VK
    64174,    # Альфа-Банк
    1122462,  # Ozon
    3776,     # Газпром нефть
    4181,     # ЛУКОЙЛ
    2180      # РЖД
]
