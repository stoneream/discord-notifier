import requests
import json


class DiscordWebHookClient:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, username, content):
        url = self.webhook_url
        headers = {"Content-Type": "application/json"}

        message = {
            "content": content,
            "username": username,
        }
        response = requests.post(url, headers=headers, data=json.dumps(message))

        if response.status_code != 204:
            raise Exception(
                f"Failed to send message: {response.status_code}, {response.text}"
            )
