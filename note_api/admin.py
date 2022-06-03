from django.contrib import admin
from .models import Note


@admin.register(Note)
class NotesAdmin(admin.ModelAdmin):
    fields = ('inner', 'state', 'is_public', 'is_important', 'publication_date', 'author')
    list_display = ('inner', 'author')
    readonly_fields = ('author',)
    list_filter = ('is_important', 'is_public', 'state')
    ordering = ('publication_date', 'is_important',)

    def has_change_permission(self, request, obj=None):
        user = request.user
        if user.is_superuser:
            return True
        if obj is not None:
            if user.id == obj.author_id:
                return True
        return False

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save(edit_by=request.user.id)
