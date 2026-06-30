from django.conf import settings
from eventregistry import EventRegistry


class EventRegistryClient:
    """
    Wrapper around the Event Registry SDK.
    """

    def __init__(self):
        self._client = EventRegistry(
            apiKey=settings.EVENT_REGISTRY_API_KEY
        )

    @property
    def client(self):
        return self._client