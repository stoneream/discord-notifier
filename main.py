import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str)
    parser.add_argument("--app-id", type=str)
    parser.add_argument("--discord-webhook-url", type=str)
    args = parser.parse_args()

    mode = args.mode

    if mode is None:
        raise Exception("mode is required")

    if mode == "exchange-rate":
        app_id = args.app_id
        discord_webhook_url = args.discord_webhook_url

        if app_id is None:
            raise Exception("app_id is required")

        if discord_webhook_url is None:
            raise Exception("discord_webhook_url is required")

        from exchange_rate_mode import ExchangeRateMode

        ExchangeRateMode(
            app_id=app_id,
            discord_webhook_url=discord_webhook_url,
        ).execute()
    elif mode == "tenki-jp":
        from tenki_jp_mode import TenkiJpMode

        TenkiJpMode().execute()
    else:
        raise Exception(f"Unknown mode: {mode}")
