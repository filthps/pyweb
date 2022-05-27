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
    class Meta:
        verbose_name = gtlz("Заметка")
        verbose_name_plural = gtlz("Заметки")

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    is_important = models.BooleanField(default=False, verbose_name=gtlz("Важно"))
    state = models.PositiveSmallIntegerField(blank=False, choices=NOTE_STATES, default=0)
    author = models.ForeignKey(User, editable=False, on_delete=models.CASCADE, verbose_name=gtlz("Автор"))
    inner = models.TextField(blank=False, verbose_name=gtlz("Текст заметки"))
    is_public = models.BooleanField(default=False, verbose_name=gtlz("Публичная"))
    publication_date = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1),
                                            verbose_name=gtlz("Дата публикации"))

    def save(self, edit_by: int = 0, **kwargs):
        """Если запись редактируется, то обязателен именованный аргумент edit_by, с int значением - id пользователя"""
        if Note.objects.filter(id__exact=self.id, author_id__exact=self.author_id).count():
            if not edit_by:
                raise FieldError("В функцию save() не был передан обязательный именованный аргумент edit_by!")
            if not isinstance(edit_by, int):
                raise ValueError("Значение неподходящее для обязательного именованного аргумента edit_by")
            if not edit_by == self.author_id:
                raise MismatchNoteAuthor(self.author_id, edit_by)
        super().save(**kwargs)

    def __str__(self):
        end = "..." if len(self.inner) > 10 else ""
        return f"{self.inner[:10]}{end}"
