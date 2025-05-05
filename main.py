import os
import logging
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from fastapi import FastAPI, Request
import google.genai as genai
from dotenv import load_dotenv
import uvicorn

# ロギングの設定
log_level = logging.DEBUG if os.environ.get("DEBUG") else logging.INFO
logging.basicConfig(level=log_level)
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

# ユーザーごとのチャットセッションを保持
user_sessions = {}

@app.message(".*")
def handle_message(message, say):
    user_id = message.get("user")
    user_message = message["text"]

    # セッションがなければ新規作成
    if user_id not in user_sessions:
        user_sessions[user_id] = client.chats.create(model="gemini-2.0-flash-001")
    chat = user_sessions[user_id]

    try:
        response = chat.send_message(user_message)
        say(f"{response.text}")
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        say(f"エラーが発生しました: {str(e)}")

# FastAPIアプリの作成
fastapi_app = FastAPI()
handler = SlackRequestHandler(app)

@fastapi_app.post("/slack/events")
async def slack_events(request: Request):
    return await handler.handle(request)

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
