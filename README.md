# Tokyo Transit Scraper

**[English](#tokyo-transit-scraper) | [日本語](#東京交通情報スクレイパー-日本語)**

A Python-based web scraper that collects real-time train operation information for Tokyo area railways, designed to run on GitHub Actions with ultra-fast `uv` environment and optional Synology Chat notifications.

## Features

- Scrapes train delay/suspension information from Yahoo! Japan Transit
- Filters for Tokyo metropolitan area lines only (JR, Tokyo Metro, Toei, private railways)
- Outputs structured JSON data
- Automatic GitHub Pages deployment for web dashboard
- Synology Chat notifications (formatted with status tags and clickable links)
- Scheduled runs (7:30 AM, 12:00 PM, and 5:30 PM JST)
- Ultra-fast CI execution powered by `uv` and Python 3.13

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── run-scraper.yml     # Scraper + notification + Pages workflow
├── .gitignore                  # Git ignore rules
├── app.py                      # Main scraper script
├── index.html                  # Web dashboard (GitHub Pages)
├── transit_data.json           # Scraped data (auto-generated)
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── README.md                   # Project documentation
```

## Monitored Railway Lines

The scraper monitors the following Tokyo area lines:

| Category | Lines |
|----------|-------|
| JR East | Yamanote, Chuo-Sobu Local, Chuo Rapid, Keihin-Tohoku, Saikyo-Kawagoe, Shonan-Shinjuku, Ueno-Tokyo, Sobu Rapid, Keiyo, Musashino, Joban Rapid/Local, Nambu, Yokosuka |
| Tokyo Metro | Ginza, Marunouchi, Hibiya, Tozai, Chiyoda, Yurakucho, Hanzomon, Namboku, Fukutoshin |
| Toei Subway | Asakusa, Mita, Shinjuku, Oedo |
| Keio | Main, New, Sagamihara, Takao, Inokashira |
| Odakyu | Odawara, Enoshima, Tama |
| Tokyu | Toyoko, Meguro, Den-en-toshi, Oimachi, Tamagawa, Ikegami, Setagaya |
| Seibu | Ikebukuro/Chichibu, Shinjuku, Kokubunji, Tamako, Yurakucho, Haijima |
| Other | Nippori-Toneri Liner, Yurikamome, Tokyo Monorail, Tama Monorail |

## Usage

### Local Development

**Option 1: Using `uv` (Recommended - Fast & Simple)**

```bash
# Run directly with uv
uv run --with-requirements requirements.txt app.py
```

**Option 2: Using standard `venv` + `pip`**

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run scraper
python app.py
```

### Output Example

```json
{
  "update_time": "2026-08-14 08:37:21",
  "data_source": "https://transit.yahoo.co.jp/diainfo/area/4",
  "monitored_lines_count": 52,
  "issue_count": 2,
  "status": "issues_found",
  "issues": [
    {
      "line": "中央総武線(各停)",
      "status": "列車遅延",
      "detail": "信号関係点検の影響で、一部列車に遅れが出ています。",
      "url": "https://transit.yahoo.co.jp/diainfo/40/0"
    }
  ]
}
```

## GitHub Actions Workflows

| Workflow | Schedule | Description |
|----------|----------|-------------|
| Run Scraper | 7:30 AM, 12:00 PM, 5:30 PM JST | Scrapes transit data with `uv`, publishes GitHub Pages, sends Synology Chat notifications |

## Required Secrets

For GitHub Actions notifications to function, configure the following repository secret:

```
SYNOLOGY_CHAT_WEBHOOK          # Synology Chat incoming webhook URL
```

## Web Dashboard

The `index.html` file provides a lightweight web dashboard displaying the latest transit status. It is designed to be embedded in Glance or similar dashboard applications.

Features:
- Dark/Light theme auto-detection
- Responsive layout
- Click to expand line details
- Auto-refresh every 5 minutes

## Technologies

- Python 3.11+ (GitHub Actions runs on Python 3.13)
- Astral `uv` / Requests / BeautifulSoup4 / Urllib3
- GitHub Actions / GitHub Pages

---

# 東京交通情報スクレイパー (日本語)

Yahoo!路線情報から東京圏の鉄道運行情報をリアルタイムで取得するPythonスクレイパーです。GitHub Actions（`uv` による高速実行）で定期実行し、必要に応じてSynology Chatへ通知を送信します。

## 機能

- Yahoo!路線情報から遅延・運休情報を取得
- 東京都内の常用52路線を自動フィルタリング（JR、東京メトロ、都営地下鉄、大手私鉄等）
- 構造化されたJSON形式でデータ出力
- GitHub Pagesへの自動デプロイ（Webダッシュボード）
- Synology Chat通知（状態タグ・リンク付きの最適化フォーマット）
- 定期実行（毎日 7:30、12:00、17:30 JST）
- `uv` と Python 3.13 による極速CI実行

## ディレクトリ構成

```
.
├── .github/
│   └── workflows/
│       └── run-scraper.yml     # スクレイピング + 通知 + Pages更新ワークフロー
├── .gitignore                  # Git除外設定
├── app.py                      # スクレイパー本体プログラム
├── index.html                  # Webダッシュボード（GitHub Pages）
├── transit_data.json           # 取得済みデータ（自動生成）
├── requirements.txt            # Python依存パッケージ
├── LICENSE                     # MITライセンス
└── README.md                   # プロジェクト説明書
```

## 監視対象路線

本スクレイパーは東京圏の以下の路線を監視します：

| カテゴリ | 路線 |
|----------|------|
| JR東日本 | 山手線、中央総武線(各停)、中央線(快速)、京浜東北根岸線、埼京川越線、湘南新宿ライン、上野東京ライン、総武線(快速)、京葉線、武蔵野線、常磐線(快速/各停)、南武線、横須賀線 |
| 東京メトロ | 銀座線、丸ノ内線、日比谷線、東西線、千代田線、有楽町線、半蔵門線、南北線、副都心線 |
| 都営地下鉄 | 浅草線、三田線、新宿線、大江戸線 |
| 京王電鉄 | 京王線、京王新線、相模原線、高尾線、井の頭線 |
| 小田急電鉄 | 小田原線、江ノ島線、多摩線 |
| 東急電鉄 | 東横線、目黒線、田園都市線、大井町線、多摩川線、池上線、世田谷線 |
| 西武鉄道 | 池袋線・秩父線、新宿線、国分寺線、多摩湖線、有楽町線、拝島線 |
| その他 | 日暮里・舎人ライナー、ゆりかもめ線、東京モノレール線、多摩都市モノレール線 |

## 使用方法

### ローカル実行

**方法 1: `uv` を使用（推奨・高速）**

```bash
# uv で直接実行
uv run --with-requirements requirements.txt app.py
```

**方法 2: 従来の `venv` + `pip`**

```bash
# 仮想環境を作成して有効化
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux

# 依存パッケージをインストール
pip install -r requirements.txt

# スクレイパーを実行
python app.py
```

### 出力データ例

```json
{
  "update_time": "2026-08-14 08:37:21",
  "data_source": "https://transit.yahoo.co.jp/diainfo/area/4",
  "monitored_lines_count": 52,
  "issue_count": 2,
  "status": "issues_found",
  "issues": [
    {
      "line": "中央総武線(各停)",
      "status": "列車遅延",
      "detail": "信号関係点検の影響で、一部列車に遅れが出ています。",
      "url": "https://transit.yahoo.co.jp/diainfo/40/0"
    }
  ]
}
```

## GitHub Actions ワークフロー

| ワークフロー | スケジュール | 説明 |
|-------------|-------------|------|
| Run Scraper | 7:30、12:00、17:30 JST | `uv` で運行情報を取得し、Pages Artifactを公開、Synology Chatへ通知 |

## 必要なシークレット (Secrets)

通知機能を利用する場合、リポジトリの Secrets に以下を設定してください：

```
SYNOLOGY_CHAT_WEBHOOK          # Synology Chat Incoming Webhook URL
```

## Webダッシュボード

`index.html` は最新の交通情報を表示する軽量なWebダッシュボードです。Glanceなどのダッシュボードアプリに埋め込んで使用できます。

機能:
- ダーク/ライトテーマ自動検出
- レスポンシブデザイン
- クリックで各路線の詳細を展開
- 5分ごとの自動データ更新

## 使用技術

- Python 3.11+ (GitHub Actions CI: Python 3.13)
- Astral `uv` / Requests / BeautifulSoup4 / Urllib3
- GitHub Actions / GitHub Pages
