from enum import Enum


class AdminMessages(Enum):
    ADD_MOVIE = "Добавить фильм"
    GET_MOVIE_BY_CODE = "Получить фильм по коду"
    CANCEL_ADDING_MOVIE = "Отменить добавление фильма"
    CANCEL_GETTING_MOVIE = "Отменить получение фильма"
    BROADCAST_MESSAGE = "Сделать рассылку"
    CANCEL_BROADCAST = "Отменить рассылку"


class UserMessages(Enum):
    GET_MOVIE_BY_CODE = "Узнать название фильма"
    CHECK_SUBSCRIPTION = "Проверить подписку"
    CANCEL_GETTING_MOVIE = "Отменить ввод фильма"
    ALREADY_SUBSCRIBED = "✅ Подтверждено!"
    GET_MOVIE_BY_GENRE = "Подобрать фильм по жанру"
