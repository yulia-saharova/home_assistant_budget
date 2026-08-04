import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "finance_db")

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Настройки пула соединений
    POOL_SIZE = 5           # Постоянные соединения
    MAX_OVERFLOW = 10       # Дополнительные при пиковой нагрузке
    POOL_TIMEOUT = 30       # Секунды ожидания
    POOL_RECYCLE = 1800     # Пересоздавать каждые 30 минут
    
    ECHO_SQL = True         # Логирование SQL запросов

settings = Settings()

