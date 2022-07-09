/*
k2: Reverse whois lookup
by github.com/harleo — MIT License
*/

package main

import (
	"bufio"
	"log"
	"os"
	"flag"
	"fmt"
	"github.com/PuerkitoBio/goquery"
)

type registrarInfo struct {
	name string
	creation_date  string
	registrar string
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
		var domainNames[] string
		for _, domain := range whoIs[1:] {
			domainNames = append(domainNames, domain.name)

			if *printPtr {
				fmt.Printf("%s | %s | %s\n", domain.name, domain.creation_date, domain.registrar)
			}
		}
		fmt.Sprintf("[:] Writing %d domain(s) to file...\n", len(domainNames))
		writeLines(domainNames, "domains.txt")
	} else {
		fmt.Println("[!] No domains found")
	}

	fmt.Println("[:] Done.")
}