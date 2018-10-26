# KnockKnock (K2) v1.1 by https://github.com/harleo

import os
import ssl
import pandas as pd
import argparse
import json


def check_ssl(func):
    def wrap(*args, **kwargs):
        if (not os.environ.get("PYTHONHTTPSVERIFY", "") and
                getattr(ssl, "_create_unverified_context", None)):
            ssl._create_default_https_context = ssl._create_unverified_context
        return func(*args, **kwargs)

    return wrap


@check_ssl
def query(name):
    url = "https://viewdns.info/reversewhois/?q=" + name
    try:
        result = pd.read_html(url)
        return result[3][0]
    except Exception as e:
        print(
            "[!] Couldn't send query, error: '%s' exiting...\n" % e
        )
        exit()


def main(args):
    print("[:] Sending query...")
    response = query(args.name)
    print("[:] Parsing response...")
    if response[0] == "Domain Name":
        if args.display:
            iter_url = iter(response)
            next(iter_url)
            for url in iter_url:
                print(url)
        if args.save:
            saved = save_to_file(args.type, response)
            if saved:
                print("[:] Saved to domains.%s" % args.type)
        print("[:] Found %d printable domains." % (len(response) - 1))
    else:
        print("[!] No domains found, please try a different name.\n")


def save_to_file(type, response):
    saved = False
    json_decoded = json.JSONDecoder().decode(response.to_json())
    if type == "json":
        with open("domains.json", "w") as outfile:
            print("[:] Saving results to JSON file...")
            json.dump(json_decoded, outfile)
        saved = True
    elif type == "txt":
        response_items_list = [
            "%s\n" % v for k, v in json_decoded.items()
        ]
        with open("domains.txt", "w") as outfile:
            print("[:] Saving results to TXT file...")
            outfile.writelines(response_items_list)
        saved = True
    return saved


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--name", type=str, required=True,
        help="name of the individual person or company to look up."
    )
    parser.add_argument(
        "-d", "--display", default=0, action="store_true",
        help="display results to console."
    )
    parser.add_argument(
        "-s", "--save", default=0, action="store_true",
        help="save results to JSON format."
    )
    parser.add_argument(
        "-t", "--type", default="json", nargs="?",
        choices=["json", "txt"],
        help="set file type: 'json' or 'txt'. Default: '%(default)s'."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = argument_parser()
    main(args)
