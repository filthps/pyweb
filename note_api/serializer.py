from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = '__all__'
