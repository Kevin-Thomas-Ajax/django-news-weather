from django.core.cache import cache

from apps.news.constants import (
    CATEGORY_MAP,
    DEFAULT_ARTICLE_LIMIT,
)

from apps.news.exceptions import NewsServiceError

from .client import GuardianClient


class NewsService:

    def __init__(self):
        self.client = GuardianClient()

    def _normalize_article(self, article):
        fields = article.get("fields", {})

        return {
            "title": article.get("webTitle"),
            "summary": fields.get("trailText", ""),
            "image": fields.get("thumbnail"),
            "url": article.get("webUrl"),
            "source": "The Guardian",
            "published_at": article.get("webPublicationDate"),
        }

    def get_latest(
        self,
        limit=5,
    ):
        cache_key = f"latest:{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        articles = self._fetch(
            page_size=limit,
            order_by="newest",
        )
        cache.set(
            cache_key,
            articles,
            timeout=300,
        )
        return articles

    def _fetch(self, **params):
        try:
            response = self.client.request(
                **params
            )
            return [
                self._normalize_article(article)
                for article in response["response"]["results"]
            ]
        except Exception as exc:
            raise NewsServiceError(
                "Unable to fetch articles."
            ) from exc

    def get_category(
            self,
            category,
            limit=DEFAULT_ARTICLE_LIMIT,
    ):
        category = category.lower()
        if category not in CATEGORY_MAP:
            raise ValueError(
                f"Unknown category: {category}"
            )
        cache_key = f"{category}:{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        articles = self._fetch(
            section=CATEGORY_MAP[category],
            page_size=limit,
            order_by="newest",
        )

        cache.set(
            cache_key,
            articles,
            timeout=300,
        )
        return articles

    def search(
            self,
            keyword,
            limit=20,
    ):
        return self._fetch(
            q=keyword,
            page_size=limit,
        )

    def refresh_cache(self):
        categories = CATEGORY_MAP.keys()

        # Refresh latest news
        cache.delete("latest:5")
        self.get_latest()

        # Refresh each category
        for category in categories:
            cache.delete(f"{category}:{DEFAULT_ARTICLE_LIMIT}")
            self.get_category(category)