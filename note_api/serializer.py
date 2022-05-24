from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

    edit_perm = serializers.SerializerMethodField('edit_permission')
    delete_perm = serializers.SerializerMethodField('delete_permission')

    def edit_permission(self, instance):
        user = self.context.get('user')
        if user is None:
            return False
        if user.is_authenticated:
            if instance.author_id == user.id:
                return True
        return False

    def delete_permission(self, instance):
        user = self.context.get('user')
        if user is None:
            return False
        if user.is_authenticated:
            if instance.author_id == user.id:
                return True
        return False


def notes_id_serializer(notes):
    return [v.get('id') for v in notes.values('id')]

