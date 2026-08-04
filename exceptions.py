class DatabaseError(Exception):
    """ Базовое исключение БД"""

    pass


class ValidationError(DatabaseError):
    """ Ошибка валидации данных """

    pass


class NotFoundError(DatabaseError):
    """ Запись не найдена """
    
    pass


class DuplicateError(DatabaseError):
    """ Дублирующаяся запись """
    
    pass
