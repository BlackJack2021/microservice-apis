# Python 3.10.8をベースにする
FROM python:3.10.8

# 作業ディレクトリを設定
WORKDIR /app

# 環境変数を設定（Pythonが.pycファイルを作成しないようにし、Pythonの出力が直接ターミナルに出力されるようにする）
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Poetryをインストール
RUN pip install poetry

# 依存関係をコピーしてインストール
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev

# アプリケーションをコピー
COPY . .