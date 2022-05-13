import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as get_lazy_text
from rest_framework import status
from .models import Note
from .urls import AJAX_UPDATE_NOTE_STATUS


LOAD_NOTES_BUTTON_TEXT = get_lazy_text("Доступно n новых заметок!")


class NotesAjax(APIView):
    def post(self, request):
        page = request.get('time')
        if page is None:

        notes = Note.objects.all()




def load_notes_list(request):
    if request.method == "GET":
        return render(request, 'list.html', {
            'content_upload_link': AJAX_UPDATE_NOTE_STATUS,
            'text': {'load_button_text': LOAD_NOTES_BUTTON_TEXT}})
