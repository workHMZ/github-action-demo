# Yahoo! Japan Transit Scraper & OpenAI Chat Client
## (中文) Yahoo!日本交通信息爬虫 & OpenAI聊天客户端
## (日本語) Yahoo!路線情報スクレイパー & OpenAIチャットクライアント

---

### 📝 Overview / 概要

**(中文)**
这是一个包含两个主要功能的Python项目：
1.  **交通信息爬虫 (`yahoojr.py`)**: 从Yahoo! Japan Transit网站抓取关东地区的实时铁路运行信息。
2.  **OpenAI聊天客户端 (`chat.py`)**: 一个用于与OpenAI API进行交互的命令行聊天工具。

**(日本語)**
このプロジェクトは、主に2つの機能を持つPythonアプリケーションです。
1.  **路線情報スクレイパー (`yahoojr.py`)**: Yahoo!路線情報サイトから関東エリアのリアルタイム鉄道運行情報を取得します。
2.  **OpenAIチャットクライアント (`chat.py`)**: OpenAI APIと対話するためのコマンドラインチャットツールです。

---

### ✨ Features / 主な機能

#### 1. 交通信息爬虫 / 路線情報スクレイパー (`yahoojr.py`)
- **(中文)** 使用 `Selenium` 从 Yahoo! Japan Transit (Kanto Area) 抓取实时铁路运行状态。
- **(日本語)** `Selenium` を使用して、Yahoo!路線情報（関東エリア） からリアルタイムの鉄道運行状況をスクレイピングします。

- **(中文)** 自动筛选出有延迟、停运等问题的线路。
- **(日本語)** 遅延や運転見合わせなど、問題が発生している路線のみを自動的に抽出します。

- **(中文)** 以结构化的 `JSON` 格式输出结果，包含更新时间、问题线路详情等。
- **(日本語)** 更新時刻、問題のある路線の詳細などを含む、構造化された `JSON` 形式で結果を出力します。

#### 2. OpenAI聊天客户端 / OpenAIチャットクライアント (`chat.py`)
- **(中文)** 提供一个简单的命令行界面与 `gpt-4.1-nano` 模型进行对话。
- **(日本語)** `gpt-4.1-nano` モデルと対話するためのシンプルなコマンドラインインターフェースを提供します。

- **(中文)** 支持连续对话（通过传递对话ID）。
- **(日本語)** 連続した会話をサポートします（対話IDを渡すことにより）。

- **(中文)** 需要设置 `OPENAI_API_KEY` 环境变量或在 `.env` 文件中配置。
- **(日本語)** `OPENAI_API_KEY` 環境変数の設定、または `.env` ファイルでの設定が必要です。

---

### 🚀 Getting Started / 利用開始までの流れ

#### 1. Clone the Repository / リポジトリをクローン
**(中文)** 克隆此代码仓库到您的本地计算机。
**(日本語)** このリポジトリをローカルマシンにクローンします。
```bash
git clone <your-repository-url>
cd <repository-directory>
```

#### 2. Install Dependencies / 依存関係をインストール
**(中文)** 使用 `pip` 安装 `requirements.txt` 文件中列出的所有依赖项。
**(日本語)** `pip` を使用して `requirements.txt` ファイルに記載されている依存関係をすべてインストールします。
```bash
pip install -r requirements.txt
```

#### 3. Set Up API Key (for chat.py) / APIキーの設定 (chat.py用)
**(中文)** 要使用聊天客户端，您需要设置您的OpenAI API密钥。
**(日本語)** チャットクライアントを使用するには、OpenAI APIキーを設定する必要があります。

**方法1: 环境变量 / 方法1: 環境変数**
```bash
# Linux/macOS
export OPENAI_API_KEY='your-api-key-here'

# Windows (Command Prompt)
set OPENAI_API_KEY=your-api-key-here
```

**方法2: `.env` 文件 / 方法2: `.env` ファイル**
**(中文)** 在项目根目录下创建一个名为 `.env` 的文件，并添加以下内容：
**(日本語)** プロジェクトのルートディレクトリに `.env` という名前のファイルを作成し、以下の内容を追加します。
```
OPENAI_API_KEY='your-api-key-here'
```

---

### 💻 Usage / 使用方法

#### 运行交通信息爬虫 / 路線情報スクレイパーの実行
**(中文)** 运行以下命令来获取最新的交通信息。结果将以JSON格式打印在控制台中。
**(日本語)** 以下のコマンドを実行して、最新の運行情報を取得します。結果はコンソールにJSON形式で出力されます。
```bash
python yahoojr.py
```

**输出示例 / 出力例:**
```json
{
    "update_time": "2023-10-27 10:30:00",
    "data_source": "https://transit.yahoo.co.jp/diainfo/area/4",
    "issue_count": 1,
    "status": "issues_found",
    "issues": [
        {
            "line": "ＪＲ京浜東北線",
            "status": "運転見合わせ",
            "detail": "沿線火災の影響で、上下線で運転を見合わせています。"
        }
    ]
}
```
*(注: 上述输出为示例，实际内容会根据实时情况而变化。)*
*(注：上記の出力はサンプルであり、実際の内容はリアルタイムの状況に応じて変化します。)*

#### 运行聊天客户端 / チャットクライアントの実行
**(中文)** 运行以下命令启动聊天机器人。
**(日本語)** 以下のコマンドを実行して、チャットボットを起動します。
```bash
python chat.py
```
**(中文)** 您可以输入 `'quit'` 或 `'exit'` 来退出程序，输入 `'new'` 来开始新的对话。
**(日本語)** `'quit'` または `'exit'` を入力してプログラムを終了し、`'new'` を入力して新しい対話を開始できます。

---

### 🛠️ Technologies Used / 使用技術
- Python 3
- Selenium
- webdriver-manager
- OpenAI Python Library
- python-dotenv

