
# syntax=docker/dockerfile:1.7
FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive
ARG TARGETARCH  # buildx 会注入：amd64 / arm64

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        ca-certificates wget gnupg unzip \
        fonts-noto-cjk; \
    if [ "$TARGETARCH" = "amd64" ]; then \
        wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; \
        dpkg -i /tmp/chrome.deb || apt-get -y -f install; \
        rm -f /tmp/chrome.deb; \
    else \
        apt-get install -y --no-install-recommends chromium; \
    fi; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 先装依赖
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# 再拷贝源码
COPY . .

# 启动命令
CMD ["python", "app.py"]