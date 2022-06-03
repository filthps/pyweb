from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as text_
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from .serializer import NoteSerializer
from .helper import Helper
from .models import Note
from .paginator import NotePaginator
from .filters import filter_by_public, filter_by_important, filter_by_state, Ordering


class NotesList(ListAPIView, Helper):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    pagination_class = NotePaginator
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer,)

    def get_paginated_response(self, data):
        if self.is_ajax(self.headers):
            return Response({'notes': data})
        return Response({
            'notes': data, 'paginator': self.paginator.get_html_context(),
            'csrf_str': self.get_csrf(self.request),
            'url': self.request.path
        }, template_name="list.html")

    @Ordering.order_notes
    def filter_queryset(self, queryset):
        params = self.request.query_params
        if params.get('public') is not None:
            queryset = filter_by_public(queryset)
        else:
            if not self.request.user.is_authenticated:
                queryset = filter_by_public(queryset)
        if params.get('important') is not None:
            queryset = filter_by_important(queryset)
        category = params.get('category')
        if category is not None:
            queryset = filter_by_state(queryset, category)
        return queryset

    def get_serializer_context(self):
        return {'user': self.request.user}


class CreateNote(LoginRequiredMixin, TemplateView, CreateAPIView, Helper):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    template_name = "create-note.html"
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_context_data(self, **kwargs):
        return {'serializer': self.get_serializer()}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['author_id'] = request.user.id
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if self.is_ajax(request.headers):
            return Response({
                'data': serializer.data
            }, template_name=None,
                status=status.HTTP_201_CREATED,
                headers=headers)
        return redirect("notes-list")


class EditNote(LoginRequiredMixin, UpdateAPIView, TemplateView, Helper):
    template_name = "edit.html"
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (TemplateHTMLRenderer,)

    def get_context_data(self, **kwargs):
        return {'form': self.get_serializer(**kwargs)}

    def perform_update(self, serializer):
        super().perform_update(serializer)
        messages.add_message(
            self.request,
            messages.INFO,
            f"{text_('Заметка')} {self.request.query_params['note_id']} {text_('изменена')}!"
        )

    def dispatch(self, request, *args, **kwargs):
        method_name: str = self.request.POST.get('_method')
        if method_name is not None and type(method_name) is str:
            method = getattr(self, method_name.lower())
            if method is not None:
                return method(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class DeleteNote(LoginRequiredMixin, DestroyAPIView, Helper):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_queryset()
        if isinstance(obj, Response):
            return obj
        self.perform_destroy(obj)
        if self.is_ajax(request.headers):
            return Response({'id': self.request.query_params['note_id']},
                            status=status.HTTP_204_NO_CONTENT)
        messages.add_message(request, messages.INFO,
                             f"{text_('Заметка')}{self.request.query_params['note_id']} {text_('удалена')}!"
                             )
        return redirect("notes-list")

    def get_object(self):
        note_id = self.request.query_params.get('note_id')
        if note_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        instance = queryset.filter(id=note_id)
        if not instance.count():
            return Response(status=status.HTTP_404_NOT_FOUND)
        return instance[0]





class AboutPage(TemplateView):
    template_name = "about.html"
