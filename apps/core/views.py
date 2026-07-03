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

    # Fetch each category only once
    business_news = news_service.get_category("business")
    sports_news = news_service.get_category("sports")
    technology_news = news_service.get_category("technology")
    health_news = news_service.get_category("health")
    entertainment_news = news_service.get_category("entertainment")

    # Use the first article from each category for the hero slider
    latest_news = []

    for articles in [
        business_news,
        sports_news,
        technology_news,
        health_news,
        entertainment_news,
    ]:
        if articles:
            latest_news.append(articles[0])

    context = {

        "navigation": navigation,

        "latest_news": news_service.get_latest(),

    }

    return render(
        request,
        "core/home.html",
        context,
    )
