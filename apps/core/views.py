from django.shortcuts import render

from apps.news.services.news_service import NewsService


def home(request):

    news_service = NewsService()

    navigation = [
        {"label": "Latest", "id": "latest"},
        {"label": "Business", "id": "business"},
        {"label": "Sports", "id": "sports"},
        {"label": "Technology", "id": "technology"},
        {"label": "Health", "id": "health"},
        {"label": "Entertainment", "id": "entertainment"},
    ]

    context = {
        "navigation": navigation,

        "business_news": news_service.get_category("business"),
        "sports_news": news_service.get_category("sports"),
        "technology_news": news_service.get_category("technology"),
        "health_news": news_service.get_category("health"),
        "entertainment_news": news_service.get_category("entertainment"),
    }

    return render(
        request,
        "core/home.html",
        context
    )
