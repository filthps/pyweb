from django.urls import path
from .views import NotesList, CheckNewNotes, NotesLoader, CreateNote, AboutPage

urlpatterns = [
    path('', NotesList.as_view(), name="notes-list"),
    path('all/check-notes/', CheckNewNotes.as_view(), name='find-new-notes'),
    path('all/load-notes/', NotesLoader.as_view(), name='load-notes'),
    path('create/', CreateNote.as_view(), name='create-note'),
    path('about/', AboutPage.as_view(), name='about')
]
