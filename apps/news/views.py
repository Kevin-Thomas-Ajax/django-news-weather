from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .services.news_service import NewsService


def category(request, category):
    service = NewsService()

    articles = service.get_category(
        category,
        limit=20,
    )

    return render(
        request,
        "news/category.html",
        {
            "category": category.title(),
            "articles": articles,
        },
    )


def lazy_category(request, category):
    service = NewsService()

    articles = service.get_category(category)

    html = render_to_string(
        "includes/news_cards.html",
        {
            "articles": articles,
        },
        request=request,
    )

    return HttpResponse(html)
