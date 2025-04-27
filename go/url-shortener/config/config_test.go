package config

import (
	"testing"
)

func TestReadConfig(t *testing.T) {
	t.Run("Default Path", func(t *testing.T) {
		// Set up
		expectedUrl := "https://www.twitter.com/status/987654321"
		c := Config{}
		c.LoadShortenUrl("./testdata/shorten_urls.yaml")

		shortenTwitterUrl, _ := c.ReadShortenUrl("uqze")

		if shortenTwitterUrl != expectedUrl {
			t.Errorf("Expected %s, got %s", expectedUrl, shortenTwitterUrl)
		}

	})

}
