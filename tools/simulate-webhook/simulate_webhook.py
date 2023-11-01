import os
import sys
import requests
import json

server_ip = sys.argv[1]
event_folder_name = sys.argv[2]

event_directory = f"../../docs/docusign-events/{event_folder_name}"
events = sorted(os.listdir(event_directory))

url = f"{server_ip}/docusign/webhook"

headers = {
    'Content-Type': 'application/json',
}

for event in events:

    # ignore any non-json files
    if not event.endswith(".json"):
        continue

    with open(f"{event_directory}/{event}", "r") as f:
        data = json.load(f)
        res = requests.post(url, headers=headers, json=data)
        if res.status_code != 200:
            print(f"Failed event with status code {res.status_code}: {event}", file=sys.stderr)
            continue
        print(f"Success event {event}")

