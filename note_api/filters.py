from django.db.models import Manager, QuerySet
from .models import Note


def get_all(m: Manager) -> QuerySet:
    ...

