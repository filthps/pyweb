from django.urls import path
from .views import NotesList, NotesLoader, CheckNewNotes, LoadNoteListPage, AJAX_CHECK_NOTES_URL


urlpatterns = [
    path('all', LoadNoteListPage.as_view()),
    path('all/<int:page>/', NotesList.as_view()),
    path(f'{AJAX_CHECK_NOTES_URL}/', CheckNewNotes.as_view()),
]
