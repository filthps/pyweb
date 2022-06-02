from django.urls import path
from .views import NotesList, CreateNote, AboutPage
from .async_views import CheckNewNotes, NotesLoader


urlpatterns = [
    path('', NotesList.as_view(), name='notes-list'),
    path('create/', CreateNote.as_view(), name='create-note'),
    path('about/', AboutPage.as_view(), name='about'),
    # ajax
    path('all/check-notes/', CheckNewNotes.as_view(), name='find-new-notes'),
    path('all/load-notes/', NotesLoader.as_view(), name='load-notes'),
]
