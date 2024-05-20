from django.urls import include, path

from . import views


urlpatterns = [
    path("ai-assistant/", include("django_ai_assistant.urls")),
    path("", views.index, name="index"),
]
