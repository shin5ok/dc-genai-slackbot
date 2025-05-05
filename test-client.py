import hmac
import hashlib
import time
import requests
import os
# 1. 必要な値を用意
signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
url = "http://localhost:3000/slack/events"
body = {
    "type": "event_callback",
    "team_id": "TCAP5P4EQ",
    "event": {
        "type": "message",
        "text": "こんにちは！",
        "user": "U12345678",
        "channel": "C0198T0DP4N", #kawano
        "ts": "1234567890.123456"
    }
}

import json
body_str = json.dumps(body, separators=(',', ':'))  # Slackは余計なスペースなしで送る

# 2. タイムスタンプを用意
timestamp = str(int(time.time()))

# 3. 署名ベース文字列を作成
basestring = f"v0:{timestamp}:{body_str}"

# 4. HMAC SHA256で署名を生成
signature = "v0=" + hmac.new(
    signing_secret.encode(),
    basestring.encode(),
    hashlib.sha256
).hexdigest()

# 5. ヘッダーを作成
headers = {
    "Content-Type": "application/json",
    "X-Slack-Request-Timestamp": timestamp,
    "X-Slack-Signature": signature
}

# 6. POSTリクエスト送信
response = requests.post(url, headers=headers, data=body_str)
print(response.status_code)
print(response.text)