import requests
import json
import csv
import time
from datetime import datetime

def get_apes(next=None):
    url = "https://api.opensea.io/api/v2/events/collection/boredapeyachtclub?after=1619827200&before=1656547200&event_type=sale"
    if next:
        suburl= f"&next={next}"
        url = url + suburl
    headers = {
    "accept": "application/json",
    "x-api-key": "a42e21a88cc247d1a29fbb44dacddebf"
    }
    response = requests.get(url, headers=headers)
    response = response.json()
    page = response["next"]
    data = response["asset_events"]
    try:
        for sale in data:
            event = {
                "id": sale["nft"]["identifier"],
                "timestamp": datetime.utcfromtimestamp(sale["event_timestamp"]).strftime('%Y-%m-%d %H:%M:%S UTC')
            }
            save_ape(event)
    except TypeError:
        pass

    if len(page) > 10:
        time.sleep(1.5)
        get_apes(page)
    else:
        return

def save_ape(event):
    with open("apes5.csv", "a+", encoding="UTF-8", newline="") as file:  # output file name
        fieldnames = ["id", "timestamp"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(event)

if __name__ == "__main__":
    get_apes()