import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- 設定 ---
TARGET_URL = "https://transit.yahoo.co.jp/diainfo/area/4"
OUTPUT_FILE = Path("transit_data.json")

# 東京都内常用路線のホワイトリスト
TOKYO_LINES = {
    # JR東日本（東京都内常用路線）
    "山手線",
    "中央総武線(各停)",
    "中央線(快速)[東京～高尾]",
    "京浜東北根岸線",
    "埼京川越線[羽沢横浜国大～川越]",
    "湘南新宿ライン",
    "上野東京ライン",
    "総武線(快速)[東京～千葉]",
    "京葉線",
    "武蔵野線",
    "常磐線(快速)[品川～取手]",
    "常磐線(各停)",
    "南武線[川崎～立川]",
    "横須賀線",
    
    # 東京メトロ
    "東京メトロ銀座線",
    "東京メトロ丸ノ内線",
    "東京メトロ日比谷線",
    "東京メトロ東西線",
    "東京メトロ千代田線",
    "東京メトロ有楽町線",
    "東京メトロ半蔵門線",
    "東京メトロ南北線",
    "東京メトロ副都心線",
    
    # 都営地下鉄
    "都営浅草線",
    "都営三田線",
    "都営新宿線",
    "都営大江戸線",
    
    # 京王電鉄
    "京王線",
    "京王新線",
    "京王相模原線",
    "京王高尾線",
    "京王井の頭線",
    
    # 小田急電鉄
    "小田急小田原線",
    "小田急江ノ島線",
    "小田急多摩線",
    
    # 東急電鉄
    "東急東横線",
    "東急目黒線",
    "東急田園都市線",
    "東急大井町線",
    "東急多摩川線",
    "東急池上線",
    "東急世田谷線",
    
    # 西武鉄道
    "西武池袋線・秩父線",
    "西武新宿線",
    "西武国分寺線",
    "西武多摩湖線",
    "西武有楽町線",
    "西武拝島線",
    
    # その他東京都内便利な路線
    "日暮里・舎人ライナー",
    "ゆりかもめ線",
    "東京モノレール線",
    "多摩都市モノレール線",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
}

class TransitParseError(RuntimeError):
    pass

def create_session() -> requests.Session:
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=2,
        pool_maxsize=2,
    )
    session = requests.Session()
    session.headers.update(HEADERS)
    session.mount("https://", adapter)
    return session

def parse_trouble_rows(soup: BeautifulSoup) -> list[dict]:
    """
    Yahoo! 路線情報の「現在運行情報のある路線」から
    路線 / 状況 / 詳細を直接取得する。
    """
    # まず「現在運行情報」の領域を限定
    trouble_section = soup.find(id="mdStatusTroubleLine")
    if trouble_section is None:
        raise TransitParseError(
            "運行情報セクションが見つかりません。"
            "Yahoo! のHTML構造が変更された可能性があります。"
        )

    section_text = trouble_section.get_text(" ", strip=True)
    # 正常時
    if "事故・遅延情報はありません" in section_text:
        return []

    issues = []
    parsed_rows = 0
    for row in trouble_section.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 3:
            continue
        
        link = cells[0].find("a")
        if link:
            line_name = link.get_text(" ", strip=True)
            detail_url = urljoin(TARGET_URL, link.get("href", ""))
        else:
            line_name = cells[0].get_text(" ", strip=True)
            detail_url = TARGET_URL

        status = cells[1].get_text(" ", strip=True)
        detail = cells[2].get_text(" ", strip=True)
        
        if not line_name or not status or not detail:
            continue
            
        parsed_rows += 1

        if line_name not in TOKYO_LINES:
            continue
            
        issues.append({
            "line": line_name,
            "status": status,
            "detail": detail,
            "url": detail_url,
        })
        
    # 「問題なし」でもなく、行も取れないなら
    # all_clear と誤判定せずエラーにする
    if parsed_rows == 0:
        raise TransitParseError(
            "運行情報は存在しますが、"
            "路線情報を解析できませんでした。"
        )

    return issues

def scrape_transit_data() -> list[dict]:
    print(f"URL: {TARGET_URL} から最新の運行情報を取得中...")
    with create_session() as session:
        response = session.get(
            TARGET_URL,
            timeout=(5, 15),
        )
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        return parse_trouble_rows(soup)

def build_output(issues: list[dict]) -> dict:
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    return {
        "update_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "data_source": TARGET_URL,
        "monitored_lines_count": len(TOKYO_LINES),
        "issue_count": len(issues),
        "status": "issues_found" if issues else "all_clear",
        "issues": issues,
    }

def write_json_atomic(data: dict) -> None:
    """
    中途半端なJSONが残らないよう、一時ファイルからatomic replace。
    """
    temp_file = OUTPUT_FILE.with_suffix(".json.tmp")
    temp_file.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    temp_file.replace(OUTPUT_FILE)
    print(f"✅ {OUTPUT_FILE} を更新しました。")

def main() -> int:
    try:
        issues = scrape_transit_data()
        output = build_output(issues)
        write_json_atomic(output)
        print(json.dumps(
            output,
            ensure_ascii=False,
            indent=2,
        ))
        return 0
    except (requests.RequestException, TransitParseError) as exc:
        print(
            f"❌ 運行情報の取得に失敗しました: {exc}",
        )
        return 1

if __name__ == "__main__":
    raise SystemExit(main())