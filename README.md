# discord-notifier

Discordにいろいろ通知くん

## 使い方

```
discord-notifier -h
```

## GitHub Actions で Cron を回す

```
mkdir .github/workflows
touch .github/workflows/notify-exchange-rate.yml
```

```yaml
name: NotifyExchangeRate
on:
  workflow_dispatch:
  schedule:
    - cron: '00 1 * * *' # JST 16:00
 jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: "1.22.x"
      - name: Install dependencies
        run: go get .
      - name: Run
        run: go run . exchange-rate --discord-webhook-url ${{ secrets.DISCORD_WEBHOOK_URL }} --app-id ${{ secrets.EXCHANGE_RATE_APP_ID }}
```
