from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


def notes_id_serializer(notes):
    return [v.get("id") for v in notes.values("id")]

