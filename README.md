# Gemini Slack Bot

Geminiと会話できるSlackボットです。

## セットアップ

1. 必要なパッケージをインストール:
```bash
# uvがインストールされていない場合は、まずuvをインストール
curl -sSfL https://astral.sh/uv/install.sh | sh

# 仮想環境を作成
uv venv

# 仮想環境を有効化
# macOS/Linuxの場合
source .venv/bin/activate
# Windowsの場合
# .venv\Scripts\activate

# 依存関係をインストール
uv pip install -e .
```

2. 環境変数の設定:
以下の環境変数を設定してください：
- `SLACK_BOT_TOKEN`: Slackボットのトークン
- `SLACK_APP_TOKEN`: Slackアプリのトークン
- `GOOGLE_API_KEY`: Google Gemini APIキー

3. ボットの起動:
```bash
python main.py
```

## ローカルテスト

ローカルでテストする場合は、Vertex AI Expressモードを使用します。このモードでは、Google Cloud認証なしでAPIキーだけで動作します。

1. [Google AI Studio](https://makersuite.google.com/app/apikey)からAPIキーを取得
2. 環境変数`GOOGLE_API_KEY`にAPIキーを設定
3. ボットを起動

## 本番環境での使用

本番環境で使用する場合は、Google Cloud認証を使用することを推奨します：

1. Google Cloudプロジェクトを作成
2. Vertex AI APIを有効化
3. 環境変数を設定：
   - `GOOGLE_CLOUD_PROJECT`: プロジェクトID
   - `GOOGLE_CLOUD_LOCATION`: リージョン（デフォルト: us-central1）
4. Google Cloud CLIで認証：
   ```bash
   gcloud auth application-default login
   ```

## 使い方

1. Slackでボットをチャンネルに招待
2. ボットをメンションしてメッセージを送信
3. Geminiからの応答が返ってきます

## 注意事項

- Python 3.9以上が必要です
- ローカルテスト時はAPIキーが必要です
- 本番環境ではGoogle Cloud認証の使用を推奨します
- Slackアプリの作成とトークンの取得は[Slack API](https://api.slack.com/apps)から行えます
