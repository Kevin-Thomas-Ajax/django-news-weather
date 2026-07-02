import requests

from django.conf import settings


class GuardianClient:

    BASE_URL = "https://content.guardianapis.com/search"

    def request(self, **params):

        params["api-key"] = settings.GUARDIAN_API_KEY

        params.setdefault(
            "show-fields",
            "thumbnail,trailText"
        )

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()