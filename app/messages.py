from enum import Enum


class AdminMessages(Enum):
    ADD_MOVIE = "Добавить фильм"
    GET_MOVIE_BY_CODE = "Получить фильм по коду"
    CANCEL_ADDING_MOVIE = "Отменить добавление фильма"
    CANCEL_GETTING_MOVIE = "Отменить получение фильма"


class UserMessages(Enum):
    pass
