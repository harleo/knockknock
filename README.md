## KnockKnock
KnockKnock runs a simple reverse whois lookup which returns a list of domains owned by people or companies.

This tool is often used for reconnaissance or OSINT (Open Source Intelligence) purposes.

Please note that the results can also contain domains that are not owned by the particular target, whereas the target represents a whois guard.

### Installation
`go get -v github.com/harleo/knockknock`

_This tool requires [golang](https://golang.org/)_

### Update
`go get -u github.com/harleo/knockknock`

### Options

```console
Usage:
  -n string
        Registrant name, email or domain name of the target (Required)
  -p    Print results
```

### Example

```console
$ knockknock -n google.com -p

[:] Sending query...
028-hty.com
0512zc.cn
--- snip ---
[:] Writing 1000 domain(s) to file...
[:] Done.
```

### Disclaimer
This tool must use an external API such as ReverseWhois (which is subject to rate limiting and a maximum of 1000 domains per query) to retrieve relevant data.

---

&copy; 2020 github.com/harleo &mdash; MIT License