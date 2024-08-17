package main

import (
	"log"
	"os"

	exchangerate "gihub.com/stoneream/discord-notifier/cmd/exchange-rate"
	"github.com/urfave/cli/v2"
)

func main() {
	app := &cli.App{
		Name:  "discord-notifier",
		Usage: "",
		Flags: []cli.Flag{
			&cli.StringFlag{
				Name:     "discord-webhook-url",
				Usage:    "Discord webhook URL",
				Required: true,
			},
		},
		Commands: []*cli.Command{
			{
				Name:  "exchange-rate",
				Usage: "Get exchange rate",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:     "app-id",
						Usage:    "Open Exchange Rates App ID",
						Required: true,
					},
				},
				Action: func(c *cli.Context) error {
					exchangeRate := &exchangerate.ExchangeRate{
						AppId:             c.String("app-id"),
						DiscordWebhookURL: c.String("discord-webhook-url"),
					}

					return exchangeRate.Execute()
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
