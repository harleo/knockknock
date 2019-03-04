
## KnockKnock
KnockKnock is a simple reverse whois lookup CLI which allows you to find domain names owned by an individual person or company, often used for Open Source Intelligence (OSINT) purposes.

### Installation
Run `pipenv install`

If you do not have `pipenv` installed, install it with `pip install pipenv`

_[!] This tool requires Python 3.7 or above &mdash; use `pip3` and `python3` respectively if you have multiple version installed_

### Options

```console
Usage: k2.py [OPTIONS]

Options:
  -n, --name TEXT        Registrant name or email of the individual person or
                         company to look up.  [required]
  -d, --display          Display output to console.
  -s, --save             Save output.
  -t, --type [json|txt]  Set file type: 'json' or 'txt'.  [default: json]
  -h, --help             Show this message and exit.
```

### Example

```console
python3 k2.py -n acme.com -d

KnockKnock v1.3
[:] Sending query...
[:] Parsing response...
acme.com.cn
acme.com.hk
acme.com
acme.hk
acme.ua
[...]
suministrosacme.com
sweatersandbeyond.com
test-acme.com
thehfg.co.uk
xiaoweilu.cn
[:] Found 74 domains (maximum 500).
```

### Disclaimer
This tool is courtesy of the free tier (non-API) of ViewDNS (https://viewdns.info) which is also limited to showing 500 domains for a given query &mdash; please use responsibly.

---

&copy; 2019 Leonid Hartmann