import uuid
import datetime
from django.utils.translation import gettext_lazy as gtlz
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from .exceptions import MismatchNoteAuthor


NOTE_STATES = (
    (0, gtlz("Активнo")),
    (1, gtlz("Отложенo")),
    (2, gtlz("Выполненo")),
)


class Note(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    is_important = models.BooleanField(default=False)
    state = models.CharField(max_length=30, choices=NOTE_STATES, default=0)
    author = models.ForeignKey(User, editable=False, on_delete=models.SET_NULL, null=True)
    inner = models.TextField(blank=False)
    #  is_public
    publication_date = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1))

    def save(self, edit_by: int = 0, **kwargs):
        """Если запись редактируется, то обязателен именованный аргумент edit_by, с int значением - id пользователя"""
        note = Note.objects.filter(id__exact=self.id, author_id__exact=self.author_id)
        if note.count():
            note = note[0]
            if not edit_by:
                raise FieldError("В функцию save() не был передан обязательный именованный аргумент edit_by!")
            if not isinstance(edit_by, int):
                raise ValueError("Значение неподходящее для обязательного именованного аргумента edit_by")
            if not note.publication_date == self.publication_date:
                if not edit_by == self.author_id:
                    raise MismatchNoteAuthor(self.author_id, edit_by)
        super().save(**kwargs)
