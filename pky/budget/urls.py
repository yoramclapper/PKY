from django.urls import path

from .views import ActualsView

urlpatterns = [
    path("", ActualsView.as_view(), name="index"),
]