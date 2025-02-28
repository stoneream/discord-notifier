import requests


class OpenExchangeRateClient:
    def __init__(self, app_id):
        self.app_id = app_id
        self.host = "https://openexchangerates.org"

    def get_latest(self) -> dict:
        url = f"{self.host}/api/latest.json"
        params = {"app_id": self.app_id, "base": "USD"}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"Status code is not 200: {response.status_code}")

        return response.json()
