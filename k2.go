/*
k2: Reverse whois lookup
by github.com/harleo — MIT License
*/

package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

type registrarInfo struct {
	name          string
	creation_date string
	registrar     string
}

var whoIs []registrarInfo

func writeLines(lines []string, path string) error {
	file, err := os.Create(path)
	if err != nil {
		log.Fatalf("[!] Couldn't create domains.txt file: %s\n", err.Error())
	}
	defer file.Close()

	w := bufio.NewWriter(file)
	for _, line := range lines {
		fmt.Fprintln(w, line)
	}
	return w.Flush()
}

func main() {
	namePtr := flag.String("n", "", "Registrant name, email or domain name of the target (Required)")
	printPtr := flag.Bool("p", false, "Print results")
	outputPtr := flag.String("o", "domains.txt", "Output file to write results to")

	flag.Parse()

	if *namePtr == "" {
		flag.PrintDefaults()
		os.Exit(0)
	}

	fmt.Println("[:] Sending query...")

	doc, err := goquery.NewDocument(fmt.Sprintf("https://viewdns.info/reversewhois/?q=%s", *namePtr))
	if err != nil {
		log.Fatalf("[!] Couldn't send query request: %s\n", err.Error())
	}

	// API uses Cloudflare, most likely all cloud IPs require captcha verification whereas residential IPs are able to pass
	doc.Find("html").Each(func(_ int, body *goquery.Selection) {
		if strings.Contains(body.Text(), "Cloudflare Ray ID") {
			fmt.Println("[!] Query was blocked by Cloudflare captcha, try from a different IP.")
			os.Exit(0)
		}
	})

	doc.Find("html body font table#null tbody tr td font table tbody tr").Each(func(_ int, tr *goquery.Selection) {
		e := registrarInfo{}
		tr.Find("td").Each(func(ix int, td *goquery.Selection) {
			switch ix {
			case 0:
				e.name = td.Text()
			case 1:
				e.creation_date = td.Text()
			case 2:
				e.registrar = td.Text()
			}
		})
		whoIs = append(whoIs, e)
	})

	if len(whoIs) > 0 {
		var domainNames []string
		for _, domain := range whoIs[1:] {
			domainNames = append(domainNames, domain.name)

			if *printPtr {
				fmt.Printf("%s | %s | %s\n", domain.name, domain.creation_date, domain.registrar)
			}
		}
		fmt.Printf("[:] Writing %d domain(s) to file %s...\n", len(domainNames), *outputPtr)
		writeLines(domainNames, *outputPtr)
	} else {
		fmt.Println("[!] No domains found")
	}

	fmt.Println("[:] Done.")
}
