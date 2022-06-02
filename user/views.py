from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings


class LoginPage(APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return Response({
            'form': AuthenticationForm()
        }, template_name="login.html")

    def post(self, request: HttpRequest):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_instance = authenticate(username=data.get("username"), password=data.get("password"))
            if user_instance is None:
                return Response({'form': form}, template_name="login.html")
            login(request, user_instance)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return Response({'form': form}, template_name="login.html")
