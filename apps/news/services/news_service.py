from eventregistry import (
    QueryArticles,
    RequestArticlesInfo,
)

from apps.news.constants import (
    CATEGORY_MAP,
    DEFAULT_ARTICLE_LIMIT,
)

from apps.news.exceptions import NewsServiceError

from .client import EventRegistryClient
from django.core.cache import cache

class NewsService:

    def __init__(self):
        self.er = EventRegistryClient().client

    def _normalize_article(self, article):
        """
        Convert Event Registry article into
        our application's standard format.
        """

        return {
            "title": article.get("title", ""),
            "summary": article.get("body", ""),
            "image": article.get("image"),
            "url": article.get("url"),
            "source": article.get("source", {}).get("title", "Unknown"),
            "published_at": article.get("dateTime"),
        }

    def _fetch_articles(self, query):
        """
        Execute an Event Registry query and
        return normalized articles.
        """

        try:
            response = self.er.execQuery(query)

            articles = response.get("articles", {}).get("results", [])

            return [
                self._normalize_article(article)
                for article in articles
            ]

        except Exception as exc:
            raise NewsServiceError(
                "Unable to fetch articles."
            ) from exc

    def get_category(
            self,
            category,
            limit=DEFAULT_ARTICLE_LIMIT,
            force_refresh=False,
    ):
        category = category.lower()

        if category not in CATEGORY_MAP:
            raise ValueError(f"Unknown category: {category}")

        category_name = CATEGORY_MAP[category]

        category_uri = self.er.getCategoryUri(category_name)

        query = QueryArticles(
            categoryUri=category_uri
        )

        query.setRequestedResult(
            RequestArticlesInfo(count=limit)
        )

        cache_key = f"news:{category}:{limit}"

        if not force_refresh:

            cached = cache.get(cache_key)

            if cached is not None:
                print(f"Cache HIT -> {category}")
                return cached

        print(f"Cache MISS -> {category}")

        articles = self._fetch_articles(query)

        cache.set(
            cache_key,
            articles,
            timeout=300,  # 5 minutes
        )

        return articles

    def search(self, keyword, limit=20):
        """
        Search articles by keyword.
        """

        query = QueryArticles(
            keywords=keyword
        )

        query.setRequestedResult(
            RequestArticlesInfo(
                count=limit
            )
        )

        return self._fetch_articles(query)

    def refresh_cache(self):

        categories = [
            "business",
            "sports",
            "technology",
            "health",
            "entertainment",
        ]

        for category in categories:
            print(f"Refreshing {category}")

            self.get_category(
                category,
                limit=4,
                force_refresh=True,
            )
