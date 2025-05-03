# プロジェクト設定
PROJECT_ID := $(shell gcloud config get-value project)
REGION := asia-northeast1
SERVICE_NAME := slack-bot
REPOSITORY := slack-bot-repo
IMAGE_NAME := $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(SERVICE_NAME)

# デプロイ設定
PORT := 3000
MEMORY := 512Mi
CPU := 1
MAX_INSTANCES := 10
MIN_INSTANCES := 0

.PHONY: build deploy clean setup

# Artifact Registryのリポジトリを作成
setup:
	gcloud artifacts repositories create $(REPOSITORY) \
		--repository-format=docker \
		--location=$(REGION) \
		--description="Docker repository for Slack bot"

# Dockerイメージのビルド
build:
	docker build -t $(IMAGE_NAME) .

# Cloud Runへのデプロイ
deploy:
	gcloud run deploy $(SERVICE_NAME) \
		--image $(IMAGE_NAME) \
		--platform managed \
		--region $(REGION) \
		--port $(PORT) \
		--memory $(MEMORY) \
		--cpu $(CPU) \
		--max-instances $(MAX_INSTANCES) \
		--min-instances $(MIN_INSTANCES) \
		--allow-unauthenticated

# ローカルでの実行
run:
	docker run -p $(PORT):$(PORT) \
		-e SLACK_BOT_TOKEN=$(SLACK_BOT_TOKEN) \
		-e SLACK_SIGNING_SECRET=$(SLACK_SIGNING_SECRET) \
		-e GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT) \
		-e GOOGLE_CLOUD_LOCATION=$(GOOGLE_CLOUD_LOCATION) \
		$(IMAGE_NAME)

# イメージの削除
clean:
	docker rmi $(IMAGE_NAME) || true
	gcloud artifacts docker images delete $(IMAGE_NAME) --quiet || true 