import re
import datetime
from typing import Pattern
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from .serializer import NoteSerializer
from .helper import Helper
from .models import Note
from .paginator import NotePaginator
from .filters import filter_by_public, Ordering


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
        if not self.request.user.is_authenticated:
            queryset = filter_by_public(queryset)
        return queryset

    def get_serializer_context(self):
        return {'user': self.request.user}


class CreateNote(LoginRequiredMixin, TemplateView, CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    template_name = "create-note.html"
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_context_data(self, **kwargs):
        return {'serializer': self.get_serializer()}

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        if request.is_ajax(request.headers):
            return Response({
                'data': resp.data
            }, template_name=None)
        return Response({
            'serializer': self.get_serializer(resp.data)
        })

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.request.user})
        return context


class EditNote(APIView, UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = NoteSerializer

    def get(self, request):
        ...

    def post(self, request):
        ...


class AboutPage(TemplateView):
    template_name = "about.html"
