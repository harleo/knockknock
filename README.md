## KnockKnock

[![MIT License](https://img.shields.io/github/license/harleo/asnip?label=License&style=flat-square)](https://opensource.org/licenses/MIT)

KnockKnock runs a simple reverse whois lookup which returns a list of domains owned by people or companies.

This tool is often used for reconnaissance or OSINT (Open Source Intelligence) purposes.

Please note that the results can also contain domains that are not owned by the particular target, whereas the target represents a whois guard.

### Installation
`go install github.com/harleo/knockknock@latest`

_This tool requires [golang](https://golang.org/)_

### Options

```console
Usage:
  -n string
        Registrant name, email or domain name of the target (Required)
  -o string
        Output file to write results to (default "domains.txt")
  -p    Print results
```

### Example

```console
$ knockknock -n google.com -o google.txt -p

[:] Sending query...
028-hty.com | 2016-05-20 | DROPCATCH.COM 883 LLC
04plan.com | 2020-04-04 | GABIA, INC.
--- snip ---
[:] Writing 500 domain(s) to file google.txt...
[:] Done.
```

### Disclaimer
This tool must use an external API such as ViewDNS.info (which is subject to rate limiting and a maximum of 500 domains per query) to retrieve relevant data. Also note that the API uses Cloudflare, queries from cloud IPs may be blocked and require captcha verification whereas residential IPs are able to pass.

---

&copy; github.com/harleo