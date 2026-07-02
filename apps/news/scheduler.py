from apscheduler.schedulers.background import BackgroundScheduler

from .services.news_service import NewsService


scheduler = BackgroundScheduler()

scheduler.add_job(
    NewsService().refresh_cache,
    "interval",
    minutes=5,
)
