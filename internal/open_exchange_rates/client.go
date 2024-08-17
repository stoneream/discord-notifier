package openexchangerates

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
)

type Client struct {
	AppId string
	Host  string
}

type Latest struct {
	Disclaimer string             `json:"disclaimer"`
	License    string             `json:"license"`
	Base       string             `json:"base"`
	Timestamp  int64              `json:"timestamp"`
	Rates      map[string]float64 `json:"rates"`
}

func NewClient(appId string) *Client {
	return &Client{
		AppId: appId,
	}
}

func (c *Client) GetLatest() (*Latest, error) {
	u := &url.URL{
		Scheme: "https",
		Host:   "openexchangerates.org",
		Path:   "/api/latest.json",
	}
	query := url.Values{}
	query.Set("app_id", c.AppId)
	query.Set("base", "USD")
	u.RawQuery = query.Encode()

	client := &http.Client{}
	resp, err := client.Get(u.String())
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("status code is not 200: %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	latest := &Latest{}
	if err := json.Unmarshal(body, latest); err != nil {
		return nil, err
	}

	return latest, nil
}
