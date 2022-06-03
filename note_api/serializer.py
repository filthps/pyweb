import datetime
from rest_framework import serializers
from .models import Note
from django.conf import settings


def get_publication_date():
    t = datetime.datetime.now() + datetime.timedelta(days=1)
    return t.strftime(settings.REST_FRAMEWORK['DATETIME_FORMAT'])


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ('comments',)

    publication_date = serializers.DateTimeField(initial=get_publication_date())
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
