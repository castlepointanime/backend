# Simulate Webhook

The folder `docs/docusign-events` contains saved data of real webhook data. Use this script to send those JSONs in order to the backend.

## How to run

1. Make sure the backend is running
2. Run `python3 simulate_webhook.py {SERVER_IP} {EVENT_FOLDER_NAME}`

Example:

`python3 simulate_webhook.py http://localhost:3001 creation-workflow`
