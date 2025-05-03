# Python 3.13のベースイメージを使用
FROM python:3.13-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なツールをインストール
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# poetryのインストール
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry --version

# poetryの設定
ENV PATH="/opt/poetry/bin:$PATH"
RUN poetry config virtualenvs.create false

# 必要なパッケージをインストール
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-interaction --no-ansi --no-root

# アプリケーションコードをコピー
COPY . .

# ポートを公開
EXPOSE 3000

# アプリケーションを起動
CMD ["python", "main.py"] 