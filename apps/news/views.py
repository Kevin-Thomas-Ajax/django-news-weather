from django.shortcuts import render

from .services.news_service import NewsService


def category(request, category):

    service = NewsService()

    articles = service.get_category(
        category,
        limit=20,
    )

    context = {
        "category": category.title(),
        "articles": articles,
    }

    return render(
        request,
        "news/category.html",
        context,
    )
