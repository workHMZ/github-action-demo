# 使用官方 Python 运行时作为父镜像
FROM python:3.9-slim

# 为Debian/Ubuntu系统设置非交互式前端，防止安装过程中出现交互提示
ENV DEBIAN_FRONTEND=noninteractive

# 安装运行Selenium和Chrome所需的系统依赖
# 1. 更新apt包列表
# 2. 安装wget和gnupg，用于添加Google的软件源
# 3. 下载并添加Google的GPG密钥
# 4. 将Google Chrome的软件源添加到系统中
# 5. 再次更新apt包列表，以包含新的Google源
# 6. 安装稳定版的Google Chrome
# 7. 清理apt缓存，减小镜像体积
RUN apt-get update && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 将工作目录设置为 /app
WORKDIR /app

# 优化缓存：先复制并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再复制应用程序的其余部分
COPY . .

# 指定容器启动时运行的命令
CMD ["python", "app.py"]