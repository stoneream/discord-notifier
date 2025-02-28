from open_exchange_rate_client import OpenExchangeRateClient
from discord_webhook_client import DiscordWebHookClient
from datetime import datetime


class ExchangeRateMode:
    def __init__(self, app_id, discord_webhook_url):
        self.app_id = app_id
        self.discord_webhook_url = discord_webhook_url

    def execute(self):
        open_exchange_rate_client = OpenExchangeRateClient(app_id=self.app_id)
        discrod_webhook_client = DiscordWebHookClient(
            webhook_url=self.discord_webhook_url
        )

        latest = open_exchange_rate_client.get_latest()
        usd_jpy = latest.get("rates").get("JPY")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = """
USD/JPY: {usd_jpy}
({now})
""".format(
            usd_jpy=usd_jpy,
            now=now,
        )

        discrod_webhook_client.send_message(content=message, username="為替レート")
