package exchangerate

import (
	"fmt"
	"time"

	"gihub.com/stoneream/discord-notifier/internal/discord"
	openexchangerates "gihub.com/stoneream/discord-notifier/internal/open_exchange_rates"
)

type ExchangeRate struct {
	AppId             string
	DiscordWebhookURL string
}

func (e *ExchangeRate) Execute() error {
	discordWebHookClient := discord.NewClient(e.DiscordWebhookURL)
	openexchangeratesClient := openexchangerates.NewClient(e.AppId)

	latest, err := openexchangeratesClient.GetLatest()

	if err != nil {
		return err
	}

	content := fmt.Sprintf(`
USD/JPY : %f
(%s)
`, latest.Rates["JPY"], time.Unix(latest.Timestamp, 0))

	message := discord.Message{
		Content:  content,
		UserName: "為替レート",
	}

	if err := discordWebHookClient.SendMessage(message); err != nil {
		return err
	}

	return nil
}
