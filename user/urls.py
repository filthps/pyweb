from django.urls import path
from .views import LoginPage

urlpatterns = [
    path('', LoginPage.as_view(), name="login")
]
