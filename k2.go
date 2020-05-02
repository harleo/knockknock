/*
k2: Reverse whois lookup
by https://github.com/harleo/
*/

package main

import (
	"bufio"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/puerkitobio/goquery"
)

type sliceVal []string

func (s sliceVal) String() string {
	var str string
	for _, i := range s {
		str += fmt.Sprintf("%s\n", i)
	}
	return str
}

func writeLines(lines []string, path string) error {
	file, err := os.Create(path)
	if err != nil {
		log.Fatalf("[!] Couldn't create file: %s\n", err.Error())
	}
	defer file.Close()

	w := bufio.NewWriter(file)
	for _, line := range lines {
		fmt.Fprintln(w, line)
	}
	return w.Flush()
}

func httpRequest(URI string) string {
	response, errGet := http.Get(URI)
	if errGet != nil {
		log.Fatalf("[!] Error sending request: %s\n", errGet.Error())
	}

	responseText, errRead := ioutil.ReadAll(response.Body)
	if errRead != nil {
		log.Fatalf("[!] Error reading response: %s\n", errRead.Error())
	}

	defer response.Body.Close()
	return string(responseText)
}

func parseTable(data string) ([][]string, []string) {
	var rows [][]string
	var row []string

	doc, err := goquery.NewDocumentFromReader(strings.NewReader(data))
	if err != nil {
		log.Fatalf("[!] Parsing issue: %s\n", err.Error())
	}

	doc.Find("table").Each(func(index int, tablehtml *goquery.Selection) {
		tablehtml.Find("tr").Each(func(indextr int, rowhtml *goquery.Selection) {
			rowhtml.Find("td").Each(func(indexth int, tablecell *goquery.Selection) {
				row = append(row, tablecell.Text())
			})
			rows = append(rows, row)
			row = nil
		})
	})

	return rows, row
}

func main() {
	namePtr := flag.String("n", "", "Registrant name or email of the individual person or company (Required)")
	printPtr := flag.Bool("p", false, "Print results")
	flag.Parse()

	if *namePtr == "" {
		flag.PrintDefaults()
		os.Exit(0)
	}

	fmt.Println("[:] Sending query...")
	request := httpRequest(fmt.Sprintf("https://www.reversewhois.io/?searchterm=%s", *namePtr))
	rows, _ := parseTable(request)

	var domains []string

	if len(rows) > 0 {
		for _, domain := range rows[1:] {
			domains = append(domains, domain[1])
		}

		if *printPtr {
			fmt.Print(sliceVal(domains))
		}

		fmt.Printf("[:] Writing %d domain(s) to file...\n", len(domains))
		writeLines(domains, "domains.txt")
	} else {
		fmt.Println("[!] No domains found")
	}
}
