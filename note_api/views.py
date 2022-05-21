import re
import json
import datetime
from typing import Pattern
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as get_lazy_text
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from .serializer import notes_short_serializer, NoteSerializer
from .helper import Helper
from .models import Note
from .paginator import NotePaginator
from .urls import AJAX_CHECK_NOTES_URL


class NotesList(ListAPIView, Helper):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    pagination_class = NotePaginator
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    LOAD_NOTES_BUTTON_TEXT = get_lazy_text("Доступно n новых заметок!")

    def get_paginated_response(self, data):
        if self.is_ajax(self.headers):
            return Response(data={'notes': data})
        return Response(data={
            'notes': data, 'paginator': self.paginator.get_html_context(),
            'csrf_str': self.get_csrf(self.request),
            'content_upload_link': AJAX_CHECK_NOTES_URL,
            'url': self.request.path
        }, template_name="list.html")

    def filter_queryset(self, queryset):
        return queryset


class CheckNewNotes(APIView, Helper):
    MAX_SIZE = 20  # Максимальное количество элементов за 1 запрос

    def get(self, request):
        time = request.GET.get("time")
        if time is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.is_valid_time(time)
        notes = Note.objects.filter(publication_date__gt=self.convert_datetime_format(time))[:self.MAX_SIZE]
        notes = self.filter_notes(notes)
        return Response(data={'notes': notes_short_serializer(notes)}, status=status.HTTP_200_OK)

    @staticmethod
    def is_valid_time(time: str):
        if not str.isdigit(time):
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)

    @staticmethod
    def convert_datetime_format(ms: str):
        return datetime.datetime.fromtimestamp(int(ms) / 1000, tz=datetime.timezone.utc)

    @staticmethod
    def filter_notes(n: QuerySet):
        return n.order_by('-publication_date')


class NotesLoader(APIView, Helper):
    reg = re.compile(r'[a-f\d]{8}-[a-f\d]{4}-4[a-f\d]{3}-[89aAbB][a-f\d]{3}-[a-f\d]{12}')
    MAX_SIZE = 200  # Максимальное количество id, которое можно запросить с фронтенда рамках 1 запроса

    def post(self, request):
        data = request.POST.get('id')
        if data is None:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        parsed_data = self.parse_json(data)
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
