from django.urls import path
from .views import load_notes_list, NoteApi


AJAX_UPDATE_NOTE_STATUS = 'check-new-notes'

api_urls = [
    path('all', load_notes_list),
    path(f'{AJAX_UPDATE_NOTE_STATUS}/<int>', NoteApi.as_view())
]
