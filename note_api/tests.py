import datetime
import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from .models import Note
from .exceptions import MismatchNoteAuthor


class TestApiModelsAuthorEditPublishTime(TestCase):
    """Тестовые случаи связанные с требованием ТЗ №7"""

    USERNAME = 'somelogin'
    NOTE_ID = uuid.uuid4()

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(cls.USERNAME, 'someemail@mail.com', 'passstring')
        Note.objects.create(id=cls.NOTE_ID, inner="dfdfgdfgdb", author=user)

    def test_note_is_exist(self):
        note = Note.objects.filter(id=self.NOTE_ID)
        self.assertTrue(note.count())

    def test_exception__edit_by__kwarg(self):
        """Отсутствует аргумент edit_by"""
        note = Note.objects.get(id=self.NOTE_ID)
        note.is_important = True
        note.inner = "Some text...."
        with self.assertRaises(FieldError):
            note.save()  # edit_by

    def test_edit_publication_date(self):
        """Дату публицации редактирует НЕ автор"""
        other_user = User.objects.create_user('somelogin2', 'someem34@mail.com', 'passst5345ring')
        note = Note.objects.get(id=self.NOTE_ID)
        note.publication_date = datetime.datetime.now() + datetime.timedelta(days=4)
        with self.assertRaises(MismatchNoteAuthor):
            note.save(edit_by=other_user.id)

    def test_success_edit(self):
        user = User.objects.get(username=self.USERNAME)
        note = Note.objects.get(id=self.NOTE_ID)
        note.inner = "rsdgsdgdgdfgdsfsgsdg"
        note.publication_date = datetime.datetime.now()
        note.save(edit_by=user.id)
