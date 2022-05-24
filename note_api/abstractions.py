from abc import ABC, abstractmethod
from django.db.models import QuerySet
from .models import Note


class AbstractHelper(ABC):
    """
    Класс с публичными методами для наследования в представлениях.
    """

    @classmethod
    @abstractmethod
    def is_ajax(cls, d: dict[str, str]):
        """
        Читать словарь с header-атрибутами запроса на предмет наличия пары ключ-значение,
        наличие которой характеризаует этот запрос как асинхронный

        :return: bool()
        """

    @classmethod
    @abstractmethod
    def get_csrf(cls):
        """
        Получить строку-токен для нужд фронтенда

        :return: str
        """


class Ordering(ABC):

    __notes: QuerySet[Note] = ...

    @classmethod
    @abstractmethod
    def order_notes(cls, queryset):
        """
        :param queryset: Входящий, неотсортированный экземляр QuerySet c Notes

        :return: Отсортированный экземляр QuerySet c Notes
        """
        cls.__notes = queryset
        cls.__order_by_date()
        cls.__order_by_important()
        return cls.__notes

    @classmethod
    @abstractmethod
    def __order_by_date(cls):
        """
        Сортировать queryset по дате. Модифицируют атрибут класса __notes

        :return: None
        """
        cls.__notes = cls.__notes.order_by(...)

    @classmethod
    @abstractmethod
    def __order_by_important(cls):
        """
        Сортировать queryset по важности. Модифицируют атрибут класса __notes

        :return: None
        """
        cls.__notes = cls.__notes.order_by(...)
