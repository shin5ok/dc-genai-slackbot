import hmac
import hashlib
import time
import requests
import os
import click
import json

@click.command()
@click.argument('message')
def main(message):
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
    url = "http://localhost:3000/slack/events"

    body = {
        "type": "event_callback",
        "team_id": "TCAP5P4EQ",
        "event": {
            "type": "message",
            "text": message,
            "user": "U12345678",
            "channel": "C0198T0DP4N", #kawano
            "ts": "1234567890.123456"
        }
    }

    body_str = json.dumps(body, separators=(',', ':'))  # Slackは余計なスペースなしで送る
    timestamp = str(int(time.time()))
    basestring = f"v0:{timestamp}:{body_str}"
    signature = "v0=" + hmac.new(
        signing_secret.encode(),
        basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Slack-Request-Timestamp": timestamp,
        "X-Slack-Signature": signature
    }

    response = requests.post(url, headers=headers, data=body_str)
    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    main()