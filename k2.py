# KnockKnock by https://github.com/harleo

# Suppress false flag pylint warning about click
# pylint: disable=no-value-for-parameter

import pandas as pd
import requests
import argparse
import click
import json
import ssl
import os

version = "v1.3"

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
        result = pd.read_html(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text)
        return result[3][0]
    except Exception as e:
        print(f"[!] Couldn't send query, error: {e} exiting...\n")
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


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-n",
    "--name",
    type=str,
    required=True,
    help="Registrant name or email of the individual person or company to look up.")
@click.option("-d", "--display", is_flag=True, help="Display output to console.")
@click.option("-s", "--save", is_flag=True, help="Save output.")
@click.option(
    "-t",
    "--type",
    "output_format",
    default="json",
    show_default=True,
    type=click.Choice(["json", "txt"]),
    help="Set file type: 'json' or 'txt'."
)
def main(name, display, save, output_format):
    print(f"KnockKnock {version}")
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
            print(f"[:] Saved to domains.{output_format}")
        print(f"[:] Found {(len(response) - 1)} domains (maximum 500).")
    else:
        print("[!] No domains found, please try a different name.\n")


if __name__ == "__main__":
    main()
