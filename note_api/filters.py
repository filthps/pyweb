from typing import Callable, Iterable
from django.db.models import QuerySet
from .abstractions import Ordering as ABCOrdering
from .models import Note


def filter_by_public(queryset: QuerySet[Note]):
    return queryset.filter(is_public=True)


def filter_by_important(queryset: QuerySet[Note]):
    return queryset.filter(is_important=True)


def filter_by_state(queryset: QuerySet[Note], val: Iterable):
    return queryset.filter(state__in=val)


class Ordering(ABCOrdering):

    @classmethod
    def order_notes(cls, f: Callable = None, qs: QuerySet[Note] = None):
        if qs is not None:
            cls.__notes = qs
            return cls.__ordering()

        def wrap(*args):
            cls.__notes = f(*args)
            cls.__ordering()
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
