package htmllinkparser

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestParseFunction(t *testing.T) {
	testdataDir := "./testdata"

	err := filepath.Walk(testdataDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if !info.IsDir() && strings.HasSuffix(info.Name(), ".html") {
			t.Run(info.Name(), func(t *testing.T) {
				file, err := os.Open(path)
				if err != nil {
					t.Fatalf("Failed to open file %s: %v", path, err)
				}
				defer file.Close()

				links, err := Parse(file)
				if err != nil {
					t.Fatalf("Failed to parse file %s: %v", path, err)
				}

				// Check if links are parsed correctly (this is a placeholder, adjust as needed)
				if len(links) == 0 {
					t.Errorf("Expected links in file %s, but got none", path)
				}
			})
		}
		return nil
	})

	if err != nil {
		t.Fatalf("Failed to walk through testdata directory: %v", err)
	}
}
