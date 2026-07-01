from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path(
        "<slug:category>/",
        views.category,
        name="category",
    ),
]