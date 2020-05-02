## KnockKnock
KnockKnock runs a simple reverse whois lookup which returns a list of domains owned by an individual person or company.

This tool is often used for reconnaissance or OSINT (Open Source Intelligence) purposes.

Please note that the results can also contain domains that are not owned by the particular target, whereas the target represents a whois guard.

### Installation
`go get -u github.com/harleo/knockknock`

_This tool requires [golang](https://golang.org/)_

### Options

```console
Usage:
  -n string
        Registrant name or email of the individual person or company (Required)
  -p    Print results
```

### Example

```console
$ k2 -n google.com -p

[:] Sending query...
028-hty.com
0512zc.cn
--- snip ---
[:] Writing 1000 domain(s) to file...
```

### Disclaimer
This tool must use an external API such as ReverseWhois (which is subject to rate limiting and a maximum of 1000 domains per query) to retrieve relevant data.

---

&copy; 2020 Leonid Hartmann