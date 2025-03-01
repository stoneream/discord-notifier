import requests
import json


class DiscordWebHookClient:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, username, content, image_filepath=None):
        url = self.webhook_url

        payload = None
        files = None
        if image_filepath is not None:
            files = {
                "file": (
                    image_filepath,
                    open(image_filepath, "rb"),
                )
            }
            payload = {
                "content": content,
                "username": username,
                "embeds": []
            }
        else:
            payload = {
                "content": content,
                "username": username,
            }

        response = requests.post(
            url,
            data=payload,
            files=files
        )

        if response.status_code != 204 and response.status_code != 200:
            raise Exception(
                f"Failed to send message: {response.status_code}, {response.text}"
            )
