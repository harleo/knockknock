# KnockKnock (K2) v1.2 by https://github.com/harleo

import argparse
import json
import os
import ssl

import click

import pandas as pd


def check_ssl(func):
    def wrap(*args, **kwargs):
        if not os.environ.get("PYTHONHTTPSVERIFY", "") and getattr(
            ssl, "_create_unverified_context", None
        ):
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
        print("[!] Couldn't send query, error: '%s' exiting...\n" % e)
        exit()


def save_to_file(type, response):
    json_decoded = json.JSONDecoder().decode(response.to_json())
    if type == "json":
        with open("domains.json", "w") as outfile:
            print("[:] Saving results to JSON file...")
            json.dump(json_decoded, outfile)
    elif type == "txt":
        response_items_list = ["%s\n" % v for k, v in json_decoded.items()]
        with open("domains.txt", "w") as outfile:
            print("[:] Saving results to TXT file...")
            outfile.writelines(response_items_list)


@click.command()
@click.option(
    "-n",
    "--name",
    type=str,
    required=True,
    help="name of the individual person or company to look up.",
)
@click.option("-d", "--display", is_flag=True, help="display results to console.")
@click.option("-s", "--save", is_flag=True, help="save results to JSON format.")
@click.option(
    "-t",
    "--type",
    "output_format",
    default="json",
    type=click.Choice(["json", "txt"]),
    help="set file type: 'json' or 'txt'. Default: '%(default)s'.",
)
def main(name, display, save, output_format):
    print("[:] Sending query...")
    response = query(name)
    print("[:] Parsing response...")
    if response[0] == "Domain Name":
        if display:
            iter_url = iter(response)
            next(iter_url)
            for url in iter_url:
                print(url)
        if save:
            save_to_file(output_format, response)
            print("[:] Saved to domains.%s" % output_format)
        print("[:] Found %d printable domains." % (len(response) - 1))
    else:
        print("[!] No domains found, please try a different name.\n")


if __name__ == "__main__":
    main()
