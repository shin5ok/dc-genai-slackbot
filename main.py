import os
import logging
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
import google.genai as genai
from dotenv import load_dotenv

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 環境変数の読み込み
load_dotenv()

# Slackアプリの初期化
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    logger=logger
)

# Vertex AIの初期化
client = genai.Client(
    vertexai=True,
    project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
)

@app.message(".*")
def handle_message(message, say):
    user_message = message["text"]
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=user_message
        )
        say(f"{response.text}")
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        say(f"エラーが発生しました: {str(e)}")

# Flaskアプリの作成
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
