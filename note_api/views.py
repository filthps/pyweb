import re
import datetime
from typing import Pattern
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import QuerySet
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from .serializer import notes_id_serializer, NoteSerializer
from .helper import Helper
from .models import Note
from .paginator import NotePaginator
from .filters import filter_by_public, Ordering


MAX_SIZE_NOTES = 20  # Максимальное количество notes в рамках одного запроса


class NotesList(ListAPIView, Helper):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    pagination_class = NotePaginator
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer,)

    def get_paginated_response(self, data):
        if self.is_ajax(self.headers):
            return Response({'notes': data})
        return Response({
            'notes': data, 'paginator': self.paginator.get_html_context(),
            'csrf_str': self.get_csrf(self.request),
            'url': self.request.path
        }, template_name="list.html")

    @Ordering.order_notes
    def filter_queryset(self, queryset):
        if not self.request.user.is_authenticated:
            queryset = filter_by_public(queryset)
        return queryset

    def get_serializer_context(self):
        return {'user': self.request.user}


class CheckNewNotes(APIView, Helper):
    MAX_SIZE = MAX_SIZE_NOTES

    def get(self, request):
        time = request.GET.get("time")
        if time is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.is_valid_time(time)
        notes = Note.objects.filter(publication_date__gt=self.convert_datetime_format(time))[:self.MAX_SIZE]
        notes = self.filter_notes(notes)
        return Response(data={'notes': notes_id_serializer(notes)}, status=status.HTTP_200_OK)

    @staticmethod
    def is_valid_time(time: str):
        if not str.isdigit(time):
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)

    @staticmethod
    def convert_datetime_format(ms: str):
        return datetime.datetime.fromtimestamp(int(ms) / 1000, tz=datetime.timezone.utc)

    @Ordering.order_notes
    def filter_notes(self, n: QuerySet):
        if self.request.user.is_authenticated:
            return n
        return filter_by_public(n)


class NotesLoader(APIView, Helper):
    reg = re.compile(r'[a-f\d]{8}-[a-f\d]{4}-4[a-f\d]{3}-[89aAbB][a-f\d]{3}-[a-f\d]{12}')
    MAX_SIZE = MAX_SIZE_NOTES

    def post(self, request):
        data = request.POST.get('id')
        if data is None:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        cleaned_data = tuple(filter(lambda x: self.is_valid_uuid(self.reg, x), self.parse_json(data)))
        if cleaned_data:
            if len(cleaned_data) > self.MAX_SIZE:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            notes = Note.objects.filter(id__in=cleaned_data)
            notes = Ordering.order_notes(qs=notes)
            serializer = NoteSerializer(notes, context={'user': request.user})
            return Response(serializer.data)
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def is_valid_uuid(r: Pattern, id_: str) -> bool:
        return bool(r.match(id_))


class CreateNote(APIView, Helper):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer,)

    def get(self, request):
        return Response({
            'serializer': NoteSerializer(),
            'form_url': reverse("create-note")}, template_name='create-note.html')

    def post(self, request):
        serializer = NoteSerializer(data=request.data, context={'user': request.user})
        if not serializer.is_valid():
            return Response({'serializer': serializer}, template_name='create-note.html', status=status.HTTP_200_OK)
        serializer.save()
        if self.is_ajax(request.headers):
            return Response({'created_note': serializer.data}, status=status.HTTP_201_CREATED)
        return redirect('notes-list')


class EditNote(APIView, UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = NoteSerializer

    def get(self, request):
        ...

    def post(self, request):
        ...


class AboutPage(TemplateView):
    template_name = "about.html"
