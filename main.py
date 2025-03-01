import argparse

def str2bool(v: str) -> bool:
    return v.lower() in ["true", "1", "yes", "y"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str)
    parser.add_argument("--app-id", type=str)
    parser.add_argument("--discord-webhook-url", type=str)
    parser.add_argument("--chromedriver_path", type=str)
    parser.add_argument("--dry-run", type=str2bool, default=False)
    args = parser.parse_args()

    mode = args.mode

    if mode is None:
        raise Exception("mode is required")

    if mode == "exchange-rate":
        app_id = args.app_id
        discord_webhook_url = args.discord_webhook_url

        # 必須パラメーターのチェック
        if app_id is None:
            raise Exception("app-id is required")
        if discord_webhook_url is None:
            raise Exception("discord-webhook-url is required")

        from exchange_rate_mode import ExchangeRateMode

        ExchangeRateMode(
            app_id=app_id,
            discord_webhook_url=discord_webhook_url,
        ).execute()
    elif mode == "tenki-jp":
        chromedriver_path = args.chromedriver_path
        discord_webhook_url = args.discord_webhook_url
        dry_run = args.dry_run

        print(f"--chromedriver-path: {chromedriver_path}")
        print(f"--dry-run: {dry_run}")

        # ドライランが有効な場合、discordへの通知は行わないためWebHookURLは不要
        if dry_run is True and discord_webhook_url is None:
            raise Exception("discord-webhook-url is required")
        else:
            pass

        # ドライバー未指定の場合はデフォルトのパスを指定
        if chromedriver_path is None:
            crhoemdriver_path = "/usr/bin/chromedriver"
        else:
            pass

        from tenki_jp_mode import TenkiJpMode

        TenkiJpMode(
            chromedriver_path=crhoemdriver_path,
            dry_run=dry_run,
            discord_webhook_url=discord_webhook_url,
        ).execute()
    else:
        raise Exception(f"Unknown mode: {mode}")
