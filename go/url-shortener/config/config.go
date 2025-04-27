package config

import (
	"fmt"
	"os"
	"strings"

	"gopkg.in/yaml.v3"
)

const DefaultConfigPath = ".env"
const DefaultShortenUrlsPath = "shorten_urls.yaml"

type Config struct {
	config    map[string]string
	shortener map[string]string
}

func (c *Config) LoadConfig(path string) {
	if path == "" {
		path = DefaultConfigPath
	}

	data, err := os.ReadFile(path)

	if err != nil {
		panic(err)
	}

	for line := range strings.SplitSeq(string(data), "\n") {
		fmt.Println(line)
	}
}

func (c *Config) LoadShortenUrl(path string) {
	if path == "" {
		path = DefaultShortenUrlsPath
	}

	data, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}

	var shorternerMap map[string]map[string]string
	err = yaml.Unmarshal(data, &shorternerMap)

	if err != nil {
		panic(err)
	}

	c.shortener = shorternerMap["shorten_urls"]

}

func (c *Config) ReadShortenUrl(path string) (string, error) {
	value, exists := c.shortener[path]
	if !exists {
		return "", fmt.Errorf("key not found")
	}

	return value, nil
}

func (c *Config) GetConfig(path string) string {
	value, exists := c.config[path]
	if !exists {
		return os.Getenv(path)
	}

	return value

}
