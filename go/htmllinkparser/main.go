package htmllinkparser

import (
	"io"

	"golang.org/x/net/html"
)

type Link struct {
	Href string
	Text string
}

func Parse(r io.Reader) ([]Link, error) {
	doc, err := html.Parse(r)

	if err != nil {
		panic(err)
	}

	links := make([]Link, 0)

	for n := range doc.Descendants() {
		if n.Type == html.ElementNode && n.Data == "a" {
			link := Link{}
			for _, attr := range n.Attr {
				if attr.Key == "href" {
					link.Href = attr.Val
				}
			}
			link.Text = n.FirstChild.Data
			links = append(links, link)
		}
	}

	return links, nil
}

// func main() {
// 	htmlToParse := os.Args[1]

// 	reader, err := os.Open(htmlToParse)

// 	if err != nil {
// 		panic(err)
// 	}

// 	defer reader.Close()

// 	Parse(reader)

// }
