from django.urls import path
from .views import NotesList, CreateNote, AboutPage, EditNote, DeleteNote
from .async_views import CheckNewNotes, NotesLoader


urlpatterns = [
    path('', NotesList.as_view(), name='notes-list'),
    path('create/', CreateNote.as_view(), name='create-note'),
    path('edit/', EditNote.as_view(), name="edit-note"),
    path('delete/', DeleteNote.as_view(), name="remove-note"),
    path('about/', AboutPage.as_view(), name='about'),
    # ajax
    path('all/check-notes/', CheckNewNotes.as_view(), name='find-new-notes'),
    path('all/load-notes/', NotesLoader.as_view(), name='load-notes'),
]
