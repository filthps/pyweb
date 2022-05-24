from typing import Callable
from django.db.models import QuerySet
from .abstractions import Ordering as ABCOrdering
from .models import Note


def filter_by_public(queryset: QuerySet[Note]):
    return queryset.filter(is_public=True)


class Ordering(ABCOrdering):

    @classmethod
    def order_notes(cls, f: Callable, qs: QuerySet[Note] = None):
        if qs is not None:
            cls.__notes = qs
            return cls.__ordering()

        def wrap(*args):
            cls.__notes = f(*args)
            return cls.__notes
        return wrap

    @classmethod
    def __ordering(cls):
        cls.__order_by_date()
        cls.__order_by_important()
        return cls.__notes

    @classmethod
    def __order_by_date(cls):
        cls.__notes = cls.__notes.filter()

    @classmethod
    def __order_by_important(cls):
        cls.__notes = cls.__notes.filter()
