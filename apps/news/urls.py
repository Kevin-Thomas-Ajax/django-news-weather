from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path(
        "<slug:category>/",
        views.category,
        name="category",
    ),

    path(
        "lazy/<slug:category>/",
        views.lazy_category,
        name="lazy_category",
    ),
]
