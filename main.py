import os
import logging
from slack_bolt import App
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

@app.message("*")
def handle_message(message, say):
    # メッセージを取得
    user_message = message["text"]
    
    try:
        # Geminiにメッセージを送信
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=user_message
        )
        
        # 応答をSlackに送信
        say(f"{response.text}")
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        say(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
