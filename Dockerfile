FROM python:3.11-slim

WORKDIR /app

# 依存ライブラリのコピーとインストール
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]