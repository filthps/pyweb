import re
import json
import datetime
from typing import Pattern
from django.template.context_processors import csrf
from rest_framework.views import APIView
from django.views.generic import TemplateView, ListView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as get_lazy_text
from .models import Note
from .serializer import *


PAGINATION = 2
AJAX_CHECK_NOTES_URL = 'check-new'


class Helper:
    @staticmethod
    def parse_json(data: str):
        return json.loads(data)

    @staticmethod
    def is_ajax(header):
        pass

    @staticmethod
    def get_token(r):
        return csrf(r).get('csrf_token')


class CheckNewNotes(APIView, Helper):
    def post(self, request):
        ms = request.POST.get('time')
        if ms is None:
            notes = Note.objects.all()[:PAGINATION]
            data = note_serializer_id(notes)
            return Response(data, status=status.HTTP_200_OK)
        self.is_valid_time(ms)
        notes = Note.objects.filter(publication_date__gt=self.convert_datetime_format(ms))[:PAGINATION]
        data = NoteSerializer(notes, many=True)
        return Response(data, status=status.HTTP_200_OK)

    @staticmethod
    def is_valid_time(time: str):
        if not str.isdigit(time):
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)

    @staticmethod
    def convert_datetime_format(ms: str):
        return datetime.datetime.fromtimestamp(int(ms) / 1000, tz=datetime.timezone.utc)


class NotesList(ListView, Helper):
    model = Note
    paginate_by = PAGINATION
    template_name = "list.html"

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = get_lazy_text("Страниgitца списка Notes")
        context['csrf_str'] = self.get_token(self.request)
        return context


class NotesLoader(APIView, Helper):
    reg = re.compile(r'[a-f\d]{8}-[a-f\d]{4}-4[a-f\d]{3}-[89aAbB][a-f\d]{3}-[a-f\d]{12}')
    MAX_SIZE = 200  # Максимальное количество id, которое можно запросить с фронтенда рамках 1 запроса

    def post(self, request):
        data = request.POST.get('id')
        if data is None:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        cleaned_data = tuple(self.is_valid_uuid(self.reg, x) for x in self.parse_json(data))
        if cleaned_data:
            if len(cleaned_data) > self.MAX_SIZE:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            notes = Note.objects.filter(id__in=cleaned_data)
            return Response(json.dumps({
                'notes': NoteSerializer(notes),
                'time': datetime.datetime.now().microsecond
            }))
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def is_valid_uuid(r: Pattern, id_: str) -> bool:
        return bool(r.match(id_))


class LoadNoteListPage(TemplateView, Helper):
    template_name = "list.html"
    LOAD_NOTES_BUTTON_TEXT = get_lazy_text("Доступно n новых заметок!")

    def get_context_data(self):
        return {'content_upload_link': AJAX_CHECK_NOTES_URL, 'text': {'load_button_text': self.LOAD_NOTES_BUTTON_TEXT},
                'tittle': get_lazy_text("Страница списка Notes"), 'csrf_str': self.get_token(self.request)}
