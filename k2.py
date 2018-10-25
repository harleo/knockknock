# KnockKnock (K2) v1.0 by https://github.com/harleo

import pandas as pd
import argparse
import json

def query(name):
    url = "https://viewdns.info/reversewhois/?q=" + name
    try:
        result = pd.read_html(url)
        return result[3][0]
    except:
        print("[:] Couldn't send query, exiting...\n")
        exit()

def main(name, display, save):
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
            with open("domains.json", "w") as outfile:
                print("[:] Saving results to JSON file...")
                json.dump(json.JSONDecoder().decode(response.to_json()), outfile)
        print("[:] Found %d printable domains." % (len(response) - 1))
    else:
        print("[!] No domains found, please try a different name.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", type=str, required=True, help="name of the individual person or company to look up.")
    parser.add_argument("-d", "--display", default=0, action="store_true", help="display results to console.")
    parser.add_argument("-s", "--save", default=0, action="store_true", help="save results to JSON format.")
    args = parser.parse_args()
    main(args.name, args.display, args.save)