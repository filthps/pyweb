from django.urls import path
from .views import NotesList, CheckNewNotes, AJAX_CHECK_NOTES_URL

urlpatterns = [
    path('', NotesList.as_view(), name="notes-list"),
    path(f'all/{AJAX_CHECK_NOTES_URL}/', CheckNewNotes.as_view()),
]
