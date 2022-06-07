from django.http import HttpRequest
from django import template
from django.contrib.auth.forms import AuthenticationForm


register = template.Library()


@register.simple_tag()
def login_widget(request: HttpRequest):
    if not request.user.is_authenticated:
        return AuthenticationForm()
