import re
import datetime
from typing import Pattern
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import QuerySet
from rest_framework.renderers import JSONRenderer
from .serializer import notes_id_serializer, NoteSerializer
from .helper import Helper
from .models import Note
from .filters import filter_by_public, Ordering
from .paginator import MAX_SIZE_NOTES


class CreateNoteShort(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def create(self, request, *args, **kwargs):
        if request.is_ajax(request.headers):
            serializer = NoteSerializer(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                serializer.save()
                return Response({'created_note': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'created_note': serializer.data})
        return Response(status=status.HTTP_403_FORBIDDEN)


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
