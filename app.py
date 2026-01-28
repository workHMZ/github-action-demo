import json
from datetime import datetime
import time
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- 設定 ---
logging.getLogger('WDM').setLevel(logging.WARNING)
TARGET_URL = 'https://transit.yahoo.co.jp/diainfo/area/4'
NORMAL_OPERATION_TEXT = "事故・遅延情報はありません"

def scrape_transit_data():
    """
    交通情報をスクレイピングし、全路線の情報のリストを返す。
    """
    print("Chromeブラウザを検出し、ドライバを初期化中...")
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox") # Docker/Linux環境で重要
    chrome_options.add_argument("--disable-dev-shm-usage") # Docker/Linux環境で重要
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = None
    scraped_data = []
    try:
        # webdriver-managerがChromeドライバを自動的にダウンロード・管理する
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print(f"URL: {TARGET_URL} から最新の運行情報を取得中...")
        driver.get(TARGET_URL)
        
        try:
            print("主要コンテンツの読み込みを待機中 (最長20秒)...")
            wait = WebDriverWait(driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, "contents-body")))
            print("✅ 主要コンテンツの読み込み完了。データ解析を開始します。")
        except TimeoutException:
            print("❌ 待機タイムアウト！ページの読み込みに失敗しました。")
            return None

        all_rows = driver.find_elements(By.CSS_SELECTOR, ".elmTblLstLine tr")
        
        unique_lines = set() # 重複する路線情報を防ぐためのセット

        for row in all_rows:
            if row.find_elements(By.TAG_NAME, 'th'):
                continue
            
            try:
                line_name = row.find_element(By.TAG_NAME, 'a').text.strip()
                
                # 重複チェック
                if line_name in unique_lines:
                    continue
                unique_lines.add(line_name)

                status = row.find_element(By.XPATH, './td[2]').get_attribute('textContent').strip()
                detail = row.find_element(By.XPATH, './td[3]').get_attribute('textContent').strip()
                
                scraped_data.append({
                    "line": line_name,
                    "status": status,
                    "detail": detail
                })
            except (NoSuchElementException, IndexError):
                continue
        
        return scraped_data

    except Exception as e:
        print(f"処理中に予期せぬエラーが発生しました: {e}")
        return None
    finally:
        if driver:
            driver.quit()
            print("Chromeブラウザドライバを終了しました。")

if __name__ == '__main__':
    # データをスクレイピング
    all_lines_data = scrape_transit_data()
    
    # JSON出力処理
    if all_lines_data is not None:
        # 問題がある路線のみをフィルタリング
        troubled_lines = [
            line for line in all_lines_data 
            if NORMAL_OPERATION_TEXT not in line["detail"]
        ]
        
        # 最終的なJSON構造を作成 (JST時間を使用)
        from datetime import timezone, timedelta
        JST = timezone(timedelta(hours=9))
        output_json = {
            "update_time": datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S'),
            "data_source": TARGET_URL,
            "issue_count": len(troubled_lines),
            "status": "issues_found" if troubled_lines else "all_clear",
            "issues": troubled_lines
        }
        
        # JSONを整形してプリント
        # ensure_ascii=False で日本語が文字化けしないようにする
        # indent=4 で見やすくインデントする
        print("\n--- JSON Output ---")
        print(json.dumps(output_json, ensure_ascii=False, indent=4))
        
    else:
        print("\n❌ 運行情報の取得に失敗しました。")