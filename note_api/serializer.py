from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


def note_serializer_id(note):
    return [v.get("id") for v in note.values("id")]
