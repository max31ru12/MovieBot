from os import getenv

from aiogram import Bot
from dotenv import load_dotenv


load_dotenv()

TOKEN = getenv("TOKEN")

DB_HOST = getenv("DB_HOST", default="localhost")
DB_PORT = getenv("DB_PORT", default=5432)
DB_NAME = getenv("DB_NAME", default="test")
DB_USER = getenv("DB_USER", default="test")
DB_PASSWORD = getenv("DB_PASSWORD", default="test")

CHANNEL_ONE_ID = int(getenv("CHANNEL_ONE_ID", default=-1002604536192))
CHANNEL_ONE_NAME = getenv("CHANNEL_ONE_NAME", default="Channel 1")

MOVIE_CHANNEL_ID = int(getenv("MOVIE_CHANNEL_ID", default=-1002684458709))
MOVIE_CHANNEL_NAME = getenv("CHANNEL_TWO_NAME", default="Movie channel")

bot = Bot(token=TOKEN)

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # noqa
