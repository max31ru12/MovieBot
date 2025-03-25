from os import getenv

from dotenv import load_dotenv


load_dotenv()

TOKEN = getenv("TOKEN")

DB_HOST = getenv("DB_HOST", default="localhost")
DB_PORT = getenv("DB_PORT", default=5432)
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # noqa
