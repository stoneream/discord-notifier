package discord

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/url"
)

type Client struct {
	WebhookURL string
}

type Message struct {
	Content  string `json:"content"`
	UserName string `json:"username"`
}

func NewClient(webhookURL string) *Client {
	return &Client{
		WebhookURL: webhookURL,
	}
}

func (c *Client) SendMessage(message Message) error {
	u, err := url.Parse(c.WebhookURL)
	if err != nil {
		return err
	}

	jsonBody, err := json.Marshal(message)
	if err != nil {
		return err
	}

	client := &http.Client{}
	resp, err := client.Post(u.String(), "application/json", bytes.NewReader(jsonBody))
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	return nil
}
