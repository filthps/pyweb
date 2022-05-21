from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


def notes_short_serializer(notes):
    return [{'id': v.get('id'), 'time': v.get('publication_date')} for v in notes.values('id', 'publication_date')]

